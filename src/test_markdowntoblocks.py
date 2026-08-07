import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_spacing(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_no_spacing(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_with_newline(self):
        md = """
This is **bolded** paragraph\n
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line\n
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
class TestBlockToBlockType(unittest.TestCase):
    def test_block_headings(self):
        block = """# Heading
## Heading
### Heading
#### Heading
##### Heading
###### Heading"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_code(self):
        block = """```
Code
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_block_not_code(self):
        block = """````
Code
```"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_block_quote(self):
        block = """>quote
> quote
>  quote"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_unordered_list(self):
        block = """- ul
- ul
- ul"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UL)
        
    def test_block_unordered_not_list(self):
        block = """- ul
- ul
-ul"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.UL)    
        
    def test_block_ordered_list(self):
        block = """1. ol
2. ol
3. ol"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.OL)
        
    def test_block_not_ordered_list(self):
        block = """1. ol
2. ol
5. ol"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.OL)
        
    def test_block_paragraph(self):
        block = """Paragraph"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()
