import ply.lex as lex

# Lista de terminales
tokens = (
    'BEGIN_DESCRIPTOR',
    'DESCRIPTOR_NAME',
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

if __name__ == '__main__':
    lex.runmain()
