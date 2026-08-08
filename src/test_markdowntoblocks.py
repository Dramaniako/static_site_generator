import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

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
        
class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_heading(self):
        md = """
####### h6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>h6</h6></div>",
        )
        
    def test_quote(self):
        md = """
> quote 1

>quote 2

>  quote 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote 1</blockquote><blockquote>quote 2</blockquote><blockquote>quote 3</blockquote></div>",
        )
    
    def test_ul(self):
        md = """
- li 1
-  li 2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>li 1</li><li>li 2</li></ul></div>",
        )
        
    def test_ol(self):
        md = """
1. li 1
2.  li 2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>li 1</li><li>li 2</li></ol></div>",
        )
    
if __name__ == "__main__":
    unittest.main()
