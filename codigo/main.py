import ply.lex as lex

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
t_ignore = ' \t\r\n'

# Poner todos los tokens en funciones fuerza la prioridad
# para desambiguar entre ellos.

def t_BEGIN_DESCRIPTOR(t):
    '\['
    return t

def t_DESCRIPTOR_VALUE(t):
    '"[^"]*"'
    return t

def t_END_DESCRIPTOR(t):
    ']'
    return t

def t_BEGIN_COMMENT(t):
    '{'
    return t

def t_END_COMMENT(t):
    '}'
    return t

def t_MOVE_NUMBER(t):
    '[1-9][0-9]*\.(\.\.)?'
    return t

def t_MOVE(t):
    '([PNBRQK]?[a-h]?[0-9]?x?[a-h][1-8]|O-O|O-O-O)[+#]?'
    return t

def t_GAME_RESULT(t):
    '1-0|0-1|1/2-1/2'
    return t

def t_WORD(t):
    '[^ \t\r\n}]+'
    return t

lexer = lex.lex()

import ply.yacc as yacc

def p_pgn_file(p):
    'file : descriptor_list'
    p[0] = { 'descriptor': p[1] }
    #'file : descriptor_list game'
    #p[0] = { 'descriptor': p[1], 'game': p[2] }

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
                    | MOVE move_content
                    | comment'''

def p_comment(p):
    'comment : BEGIN_COMMENT END_COMMENT'
    p[0] = ''


parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    s = sys.stdin.read()
    result = parser.parse(s)
    print(result)
