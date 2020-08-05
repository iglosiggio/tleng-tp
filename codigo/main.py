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

    if result is not None:
        print('=== Parsing results ===')
        pprint(result)
        print('=== Processing results ===')
        opening = max((count, move) for (move, count) in result['first_moves'].items())
        print('Max nesting of a comment with a valid move:', result['max_move_comment_depth'])
        print(f'Most common opening: {opening[1]} ({opening[0]} times)')
