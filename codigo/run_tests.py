import unittest
import io
import contextlib
from parser_rules import parser
from lexer_rules import lexer

class TestParser(unittest.TestCase):

    def read_and_parse_file(self, file_name):
        f = open(file_name, 'r')
        file_content = f.read()
        f.close()
        result = parser.parse(file_content, lexer)
        if result is not None:
            opening = max((count, move) for (move, count) in result['first_moves'].items())
            return [result['max_move_comment_depth'], opening[1], opening[0]]
        return result

    def test_example_pgn(self):
        result = self.read_and_parse_file("tests/example.pgn")
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 'e4')
        self.assertEqual(result[2], 1)

    def test_invalid_comment_pgn(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            result = self.read_and_parse_file("tests/invalid_comment.pgn")
        self.assertEqual(result, None)
        captured_stdout = f.getvalue().strip()
        self.assertEqual(captured_stdout, "[ERROR] Misplaced comment at line 53")

    def test_invalid_move_pgn(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            result = self.read_and_parse_file("tests/invalid_move.pgn")
        self.assertEqual(result, None)
        captured_stdout = f.getvalue().strip()
        self.assertEqual(captured_stdout, "[ERROR] Invalid move at line 57")

    def test_missing_game_result_pgn(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            result = self.read_and_parse_file("tests/missing_game_result.pgn")
        self.assertEqual(result, None)
        captured_stdout = f.getvalue().strip()
        self.assertEqual(captured_stdout, "[ERROR] Missing game result at line 0")

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
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            result = self.read_and_parse_file("tests/unfinished_comment.pgn")
        self.assertEqual(result, None)
        captured_stdout = f.getvalue().strip()
        self.assertEqual(captured_stdout, "[ERROR] Syntax error at EOF\n[ERROR] Expected token to be one of ['BEGIN_DESCRIPTOR', 'MOVE_NUMBER', 'DESCRIPTOR_VALUE', 'END_DESCRIPTOR', 'BEGIN_COMMENT', 'END_COMMENT', 'MOVE', 'GAME_RESULT', 'WORD'] instead")

if __name__ == '__main__':
    unittest.main()
