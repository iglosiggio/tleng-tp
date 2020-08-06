import unittest
from parser_rules import parser
from lexer_rules import lexer

class TestParser(unittest.TestCase):

    def read_and_parse_file(self, s) :
        f = open(s, 'r')
        s = f.read()
        f.close()
        result = parser.parse(s, lexer)
        if result is not None:
            opening = max((count, move) for (move, count) in result['first_moves'].items())
            return [result['max_move_comment_depth'], opening[1], opening[0]]
        return result

    def test_example_pgn(self):
        result = self.read_and_parse_file("tests/example.pgn")
        self.assertEqual(result[0], 1)

    def test_invalid_comment_pgn(self):
        result = self.read_and_parse_file("tests/invalid_comment.pgn")
        self.assertEqual(result, None) #TODO: deberia imprimir por pantalla el error

    def test_multiple_games_pgn(self):
        result = self.read_and_parse_file("tests/multiple_games.pgn")
        self.assertEqual(result[0], 2)
        self.assertEqual(result[1], 'e4')
        self.assertEqual(result[2], 2)

    def test_nested_comments_pgn(self):
        result = self.read_and_parse_file("tests/nested_comments.pgn")
        self.assertEqual(result[0], 2)
        self.assertEqual(result[1], 'e4')
        self.assertEqual(result[2], 1)

    def test_unfinished_comment_pgn(self):
        result = self.read_and_parse_file("tests/unfinished_comment.pgn")
        self.assertEqual(result, None)  # TODO: deberia imprimir por pantalla el error

if __name__ == '__main__':
    unittest.main()