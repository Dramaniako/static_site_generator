from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node
from split_nodes_delimiter import text_to_text_nodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    block_strings = list(filter(None, map(lambda string: string.strip(), markdown.split("\n\n"))))
    return block_strings


def block_to_block_type(block: str) -> BlockType:
    if len(re.findall(r"(^[\#]{1,} {1})", block)) != 0:
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UL
    elif all(lines[i].startswith(f"{i+1}. ") for i in range(len(lines))):
        return BlockType.OL
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_node(block, block_type))
    
    parent = ParentNode("div", children)
    return parent

def block_to_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.PARAGRAPH:        
        text_nodes = text_to_text_nodes(block.replace("\n", " "))
        html_nodes = [text_node_to_html_node(node) for node in text_nodes] 
        return ParentNode("p", html_nodes)
    
    elif block_type == BlockType.HEADING:
        heading_level = block.count("#") if block.count("#") <= 6 else 6
        text_nodes = text_to_text_nodes(re.sub(r"(^[\#]{1,} {1})", "", block))
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        
        return ParentNode(f"h{heading_level}", html_nodes)
    
    elif block_type == BlockType.CODE:
        return ParentNode("pre", [LeafNode("code", block.removeprefix("```\n").removesuffix("```"))])
    
    elif block_type == BlockType.QUOTE:
        text_nodes = text_to_text_nodes((re.sub(r"(^\> *)", "", block, 0, re.MULTILINE).replace("\n", " ")))
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    
        return ParentNode("blockquote", html_nodes)
    
    elif block_type == BlockType.UL:
        split_block = block.split("\n")
        children = []
        for each in split_block:
            text_nodes = text_to_text_nodes(re.sub(r"(^\- *)", "", each))
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            children.append(ParentNode("li", html_nodes))
        return ParentNode("ul", children)
    
    elif block_type == BlockType.OL:
        split_block = block.split("\n")
        children = []
        for each in split_block:
            text_nodes = text_to_text_nodes(re.sub(r"(^\d\. *)", "", each))
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            children.append(ParentNode("li", html_nodes))
        return ParentNode("ol", children)

    else:
        raise ValueError("block or blocktype is invalid")