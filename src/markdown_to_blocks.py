from enum import Enum
import re

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
    if len(re.findall(r"(^[\#]{1,6} {1})", block)) != 0:
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