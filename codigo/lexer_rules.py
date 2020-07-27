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