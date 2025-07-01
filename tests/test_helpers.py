# test_helpers.py
import unittest
from helpers import clean_title, clean_filename

class TestHelpers(unittest.TestCase):
    def test_clean_title_removes_file_extension(self):
        self.assertEqual(clean_title("Game%20Name.iso"), "Game Name")

    def test_clean_title_decodes_url_and_strips_trailing_symbols(self):
        self.assertEqual(clean_title("Cool%20Game%20Title%20-%20.iso"), "Cool Game Title")

    def test_clean_title_multiple_spaces_and_encoding(self):
        self.assertEqual(clean_title("Super%20Mario%20%20World%20(USA).zip"), "Super Mario World (USA)")

    def test_clean_filename_converts_spaces_and_dashes(self):
        self.assertEqual(clean_filename("Super%20Mario%20World%20-%20USA.zip"), "Super_Mario_World_USA.zip")

    def test_clean_filename_multiple_dashes_and_spaces(self):
        self.assertEqual(clean_filename("Cool%20-%20Game%20--%20Name.zip"), "Cool_Game_Name.zip")

if __name__ == '__main__':
    unittest.main()