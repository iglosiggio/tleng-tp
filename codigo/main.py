import lexer_rules
import parser_rules
from pprint import pprint

import sys

from ply.lex import lex
from ply.yacc import yacc


if __name__ == '__main__':
    
    s = sys.stdin.read()

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)
    #pp = pprint.PrettyPrinter(indent=1)
    
    result = parser.parse(s, lexer)
    print('=== Parsing results ===')
    pprint(result)
