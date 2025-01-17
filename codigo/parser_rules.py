from collections import namedtuple
from ply.yacc import yacc

from lexer_rules import tokens, Move

# It's like max(a, b) but None is the "lowest" value
def max_depth(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return max(a, b)

def increase_nesting(v):
    return v + 1 if v is not None else None

# The starting symbol for our grammar
start = 'p_pgn_file'

Descriptor = namedtuple('Descriptor', ['key', 'value'])
Comment = namedtuple('Comment', ['content', 'max_move_comment_depth'])
CommentPart = namedtuple('CommentPart', ['content', 'max_move_comment_depth'])
TurnList = namedtuple('TurnList', ['turns', 'max_move_comment_depth'])
GameTurn = namedtuple('GameTurn', ['order', 'moves', 'max_move_comment_depth'])
MoveList = namedtuple('MoveList', ['list', 'max_move_comment_depth'])

def is_str(v):
    return isinstance(v, str)

def error_rule(rule, error_message):
    def error_reporting_rule(p):
        print(f'[ERROR] {error_message} at line {p.lineno(1)}')
        raise SyntaxError
    error_reporting_rule.__doc__ = rule
    return error_reporting_rule

def p_pgn_file(p):
    'p_pgn_file : pgn_game_list'
    p[0] = p[1]

def p_pgn_game_list(p):
    '''pgn_game_list : pgn_game pgn_game_list
                     | pgn_game'''
    game_list = {}
    first_move = p[1]['first_move'].movetext

    if len(p) == 3:
        game_list['games'] = [p[1]] + p[2]['games']
        game_list['max_move_comment_depth'] = max_depth(
            p[1]['max_move_comment_depth'],
            p[2]['max_move_comment_depth']
        )
        game_list['first_moves'] = p[2]['first_moves'].copy()
        game_list['first_moves'][first_move] = game_list['first_moves'].get(first_move) + 1
    else:
        game_list['games'] = [p[1]]
        game_list['max_move_comment_depth'] = p[1]['max_move_comment_depth']
        game_list['first_moves'] = { first_move: 1 }

    p[0] = game_list

def p_pgn_game(p):
    'pgn_game : descriptor_list game'
    event_description = p[1]
    game = p[2]
    p[0] = {
        'descriptor': event_description,
        'game': game,
        # Supongo que el primer movimiento de la partida es el primer
        # movimiento del jugador blanco. Si el archivo está mal numerado o se
        # jugase con algunas reglas alternativas esto no resultaría cierto.
        'first_move': game['turns'][0].moves[0],
        'max_move_comment_depth': game['max_move_comment_depth']
    }

def p_descriptor_list(p):
    '''descriptor_list : descriptor descriptor_list
                       | descriptor'''
    tag = p[1]
    event_tags = p[2] if len(p) == 3 else {}
    event_tags[tag.key] = tag.value
    p[0] = event_tags


def p_descriptor(p):
    'descriptor : BEGIN_DESCRIPTOR any_token DESCRIPTOR_VALUE END_DESCRIPTOR'
    p[0] = Descriptor(p[2], p[3])

def p_any_token(p):
    '''any_token : BEGIN_DESCRIPTOR
                 | DESCRIPTOR_VALUE
                 | END_DESCRIPTOR
                 | BEGIN_COMMENT
                 | END_COMMENT
                 | MOVE_NUMBER
                 | MOVE
                 | GAME_RESULT
                 | WORD'''
    p[0] = p[1]

def p_game(p):
    'game : turn_list GAME_RESULT'
    p[0] = {
        'turns': p[1].turns,
        'max_move_comment_depth': p[1].max_move_comment_depth,
        'result': p[2],
    }

p_game_error_missing_result = error_rule('game : turn_list descriptor', 'Missing game result')

def p_turn_list(p):
    '''turn_list : move turn_list
                 | move'''
    turns = [p[1]]
    max_move_comment_depth = p[1].max_move_comment_depth

    if len(p) == 3:
        turns += p[2].turns
        max_move_comment_depth = max_depth(
            max_move_comment_depth,
            p[2].max_move_comment_depth
        )

    p[0] = TurnList(turns, max_move_comment_depth)

def p_move(p):
    '''move : MOVE_NUMBER MOVE
            | MOVE_NUMBER MOVE move_content'''
    order = p[1]
    moves = [p[2]]
    max_move_comment_depth = None

    if len(p) == 4:
        moves += p[3].list
        max_move_comment_depth = p[3].max_move_comment_depth

    p[0] = GameTurn(order, moves, max_move_comment_depth)

p_move_invalid_error = error_rule('move : MOVE_NUMBER WORD move_content', 'Invalid move')
p_move_mislpaced_comment_error = error_rule('move : MOVE_NUMBER comment move_content', 'Misplaced comment')

def p_move_content(p):
    '''move_content : MOVE
                    | comment
                    | MOVE move_content'''
    moves = [p[1]]
    max_move_comment_depth = None

    if isinstance(p[1], Comment):
        max_move_comment_depth = p[1].max_move_comment_depth

    if len(p) == 3:
        moves += p[2].list
        max_move_comment_depth = max_depth(
            max_move_comment_depth,
            p[2].max_move_comment_depth
        )

    p[0] = MoveList(moves, max_move_comment_depth)

p_move_content_invalid_error = error_rule('move_content : WORD', 'Invalid move')
p_move_content_invalid_error2 = error_rule('move_content : WORD move_content', 'Invalid move')

def p_comment(p):
    'comment : BEGIN_COMMENT comment_words_list END_COMMENT'
    p[0] = Comment(p[2].content, increase_nesting(p[2].max_move_comment_depth))

def p_comment_words_list(p):
    '''comment_words_list : comment_word comment_words_list
                          | comment_word'''
    if len(p) == 3:
        this_word = p[1]
        this_word_content = this_word.content
        words_list = p[2].content
        words_list_head = words_list[0]
        words_list_tail = words_list[1:]

        if is_str(this_word.content) and is_str(words_list_head):
            words_list_head = f'{this_word.content} {words_list_head}'
            content = [words_list_head] + words_list_tail
        else:
            content = [this_word_content] + words_list

        max_move_comment_depth = max_depth(
            p[1].max_move_comment_depth,
            p[2].max_move_comment_depth
        )
    else:
        content = [p[1].content]
        max_move_comment_depth = p[1].max_move_comment_depth

    p[0] = CommentPart(content, max_move_comment_depth)

def p_comment_word(p):
    '''comment_word : comment
                    | any_comment_token'''
    if isinstance(p[1], Move):
        p[0] = CommentPart(p[1], 0)
    elif isinstance(p[1], Comment):
        p[0] = CommentPart(p[1], p[1].max_move_comment_depth)
    else:
        p[0] = CommentPart(p[1], None)

def p_any_comment_token(p):
    '''any_comment_token : BEGIN_DESCRIPTOR
                         | DESCRIPTOR_VALUE
                         | END_DESCRIPTOR
                         | MOVE_NUMBER
                         | MOVE
                         | GAME_RESULT
                         | WORD'''
    p[0] = p[1]

def p_error(p):
    current_state = parser.state
    valid_actions = parser.action[parser.state].keys()

    if p is not None:
        print(f'[ERROR] Syntax error at line {p.lineno}, token={p.type} ({p.value})')
    else:
        print('[ERROR] Syntax error at EOF')
    print('[ERROR] Expected token to be one of', [action for action in valid_actions], 'instead')

parser = yacc()
