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
    'WORD',
)

t_BEGIN_DESCRIPTOR = '\['
t_DESCRIPTOR_NAME  = '[A-Z][a-zA-Z]*' # Preguntar por mail si esto está bien
t_DESCRIPTOR_VALUE = '"[^"]*"'
t_END_DESCRIPTOR   = ']'
t_BEGIN_COMMENT    = '{'
t_END_COMMENT      = '}'
t_MOVE_NUMBER      = '[1-9][0-9]*\.(\.\.)?'
t_MOVE             = '([PNBRQK]?[a-h]?[0-9]?x?[a-h][1-8]|O-O|O-O-O)(\+|\#)?'
t_ignore           = ' \t\r\n'
t_WORD             = '[^ \t\r\n]+'

lexer = lex.lex()

if __name__ == '__main__':
    lex.runmain()
