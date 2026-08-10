import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_normal(self):
        title = "# Hello"
        text = extract_title(title)
        expected = "Hello"
        self.assertEqual(text, expected)
        
    def test_extract_title_spacing(self):
        title = "#    Hello"
        text = extract_title(title)
        expected = "Hello"
        self.assertEqual(text, expected)
        
    def test_extract_title_fail(self):
        title = "## Hello"
        text = extract_title(title)
        expected = "Hello"
        self.assertNotEqual(text, expected)
        
if __name__ == "__main__":
    unittest.main()