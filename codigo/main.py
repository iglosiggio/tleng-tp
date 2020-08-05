import sys
from pprint import pprint
from parser_rules import parser
from lexer_rules import lexer

if __name__ == '__main__':
    if len(sys.argv) == 2:
        s = open(sys.argv[1]).read()
    else:
        s = sys.stdin.read()

    
    result = parser.parse(s, lexer, tracking=True, debug=False)
    print('=== Parsing results ===')
    pprint(result)
