import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    
    def test_missing_field(self):
        node = HTMLNode()
        node2 = HTMLNode(None)
        self.assertEqual(node, node2)
    
    def test_tag_eq(self):
        node = HTMLNode("h1")
        node2 = HTMLNode("h1", None)
        self.assertEqual(node, node2)
    
    def test_value_eq(self):
        node = HTMLNode("h1", "Hello THERE")
        node2 = HTMLNode("h1", "Hello THERE", None)
        self.assertEqual(node, node2)
        
    def test_children_eq(self):
        node = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")])
        node2 = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], None)
        self.assertEqual(node, node2)
  
    def test_props_eq(self):
        node = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)
        
    def test_tag_not_eq(self):
        node = HTMLNode("h1")
        node2 = HTMLNode("H1", None)
        self.assertNotEqual(node, node2)
        
    def test_value_not_eq(self):
        node = HTMLNode("h1", "Hello THERE")
        node2 = HTMLNode("h1", "HELLO THERE", None)
        self.assertNotEqual(node, node2)
        
    def test_children_not_eq(self):
        node = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE")])
        node2 = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], None)
        self.assertNotEqual(node, node2)
    
    def test_props_not_eq(self):
        node = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://WWW.google.com", "target": "_blank"})
        node2 = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)
        
    def test_props_to_html_eq(self):
        node = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html, node2.props_to_html)
        
    def test_props_to_html_not_eq(self):
        node = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://WWW.google.com", "target": "_blank"})
        node2 = HTMLNode("h1", "Hello THERE", [HTMLNode("h1", "Hello THERE"), HTMLNode("h1")], {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html, node2.props_to_html)
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")
       
    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')
        
class TestParentNode(unittest.TestCase):
    def test_parent_to_html_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_parent_to_html_props(self):
        node = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode("a", "Link", {"href": "www.google.com"}),
            ],
            {
                "href": "www.boot.dev"
            }
        )
        self.assertEqual(node.to_html(), '<a href="www.boot.dev"><b>Bold text</b>Normal text<i>italic text</i><a href="www.google.com">Link</a></a>')
     
if __name__ == "__main__":
    unittest.main()