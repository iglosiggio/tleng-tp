import ply.lex as lex

# Representación de los movimientos
class Move:
    def __init__(self, movetext):
        self.movetext = movetext
    def __str__(self):
        return self.movetext
    def __repr__(self):
        return self.movetext


# Lista de terminales
tokens = (
    'BEGIN_DESCRIPTOR',
    'DESCRIPTOR_VALUE',
    'END_DESCRIPTOR',
    'BEGIN_COMMENT',
    'END_COMMENT',
    'MOVE_NUMBER',
    'MOVE',
    'GAME_RESULT',
    'WORD',
)

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Poner todos los tokens en funciones fuerza la prioridad
# para desambiguar entre ellos.

def t_BEGIN_DESCRIPTOR(t):
    r'\['
    return t

def t_DESCRIPTOR_VALUE(t):
    r'"[^"]*"'
    return t

def t_END_DESCRIPTOR(t):
    r']'
    return t

def t_BEGIN_COMMENT(t):
    r'{'
    return t

def t_END_COMMENT(t):
    r'}'
    return t

def t_MOVE_NUMBER(t):
    r'[1-9][0-9]*\.(\.\.)?'
    return t

def t_MOVE(t):
    r'([PNBRQK]?[a-h]?[0-9]?x?[a-h][1-8]|O-O-O|O-O)[+#]?'
    t.value = Move(t.value)
    return t

def t_GAME_RESULT(t):
    r'1-0|0-1|1/2-1/2'
    return t

def t_WORD(t):
    r'[^ \t\r\n}]+'
    return t

lexer = lex.lex()

import ply.yacc as yacc

def p_pgn_file(p):
    'p_pgn_file : pgn_game_list'
    p[0] = p[1]

def p_pgn_game_list(p):
    '''pgn_game_list : pgn_game pgn_game_list
                     | pgn_game'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_pgn_game(p):
    'pgn_game : descriptor_list game'
    p[0] = { 'descriptor': p[1], 'game': p[2] }

def p_descriptor_list(p):
    '''descriptor_list : descriptor descriptor_list
                       | descriptor'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_descriptor(p):
    'descriptor : BEGIN_DESCRIPTOR any_token DESCRIPTOR_VALUE END_DESCRIPTOR'
    p[0] = { 'name': p[2], 'value': p[3] }

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
    'game : move_list GAME_RESULT'
    p[0] = { 'moves': p[1], 'result': p[2] }

def p_move_list(p):
    '''move_list : move move_list
                 | move'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_move(p):
    'move : MOVE_NUMBER move_content'
    p[0] = (p[1], p[2])

def p_move_content(p):
    '''move_content : MOVE
                    | comment
                    | MOVE move_content'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_comment(p):
    'comment : BEGIN_COMMENT comment_words_list END_COMMENT'
    p[0] = p[2]

def p_comment_words_list(p):
    '''comment_words_list : comment_word comment_words_list
                          | comment_word'''
    if len(p) == 3:
        # Juntar strings pegados
        if isinstance(p[1], str) and isinstance(p[2][0], str):
            p[0] = [f'{p[1]} {p[2][0]}'] + p[2][1:]
        else:
            p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_comment_word(p):
    '''comment_word : comment
                    | any_comment_token'''
    p[0] = p[1]


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
    if p:
        print("yacc: Syntax error at line %s, token=%s (%s)" % (p.lineno, p.type, p.value))
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    from pprint import pprint
    s = sys.stdin.read()
    result = parser.parse(s)
    print('=== Parsing results ===')
    pprint(result)
