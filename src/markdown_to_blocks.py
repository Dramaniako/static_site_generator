def markdown_to_blocks(markdown: str) -> list[str]:
    block_strings = list(filter(None, map(lambda string: string.strip(), markdown.split("\n\n"))))
    return block_strings