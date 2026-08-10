import re

def extract_title(markdown:str) -> str:
    header_line = re.search(r"(^\# *.*$[\n]?)", markdown, re.MULTILINE)
    if header_line is None:
        raise Exception("Markdown must contain header '#'")
    header_line = header_line.group(0).replace("# ", "").strip()
    return header_line

