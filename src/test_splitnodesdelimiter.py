import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_nodes_delimiter_bold(self):
        node = TextNode("**This** is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with a code block word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_nodes_delimiter_italic(self):
        node = TextNode("This is text _with a code block word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text ", TextType.TEXT),
            TextNode("with a code block word", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_nodes_delimiter_non_text(self):
        node = TextNode("`This is text with a code block word`", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("`This is text with a code block word`", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_nodes_delimiter_bold_italic(self):
        node = TextNode("**This** is text _with a code_ block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text ", TextType.TEXT),
            TextNode("with a code", TextType.ITALIC),
            TextNode(" block word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
        
if __name__ == "__main__":
    unittest.main()