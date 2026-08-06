import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    markdown_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return markdown_images

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    
    for node in old_nodes:
        extract_markdown = extract_markdown_images(node.text)
        if len(extract_markdown) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for image in extract_markdown:
            split_node = remaining.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    
            remaining = split_node[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    
    return new_nodes

def extract_markdown_links(text: str) -> list[tuple]:
    markdown_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)*", text)
    return markdown_links

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    
    for node in old_nodes:
        extract_markdown = extract_markdown_links(node.text)
        if len(extract_markdown) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for link in extract_markdown:
            split_node = remaining.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    
            remaining = split_node[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    
    return new_nodes

def text_to_text_nodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(split_nodes_link(text_nodes))
    text_nodes = split_nodes_delimiter(text_nodes, '**', TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, '_', TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, '`', TextType.CODE)
    return text_nodes