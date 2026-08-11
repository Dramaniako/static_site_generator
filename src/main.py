import os
import shutil
import re
from textnode import TextNode, TextType
from markdown_to_blocks import markdown_to_html_node
from extract_title import extract_title

def copy_content(src: str, dst: str):
    if not os.path.exists(src):
        return
    
    if not os.path.exists(dst):
        os.mkdir(dst)
    else:
        destination_items = os.listdir(dst)
        
        if len(destination_items) != 0:
            for item in destination_items:
                item_path = os.path.join(dst, item) 
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        
    
    source_items = os.listdir(src)
    
    for item in source_items:
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst)
        elif os.path.isdir(item_path):
            new_destination = os.path.join(dst, item)
            os.mkdir(new_destination)
            copy_content(item_path, new_destination)
            
def generate_page(from_path:str, template_path:str, dest_path:str):
    file_path = dest_path.replace("md", "html")
    print(f"Generating page from {from_path} to {file_path} using {template_path}")
    
    with open(from_path, "r") as markdown_file, open(template_path, "r") as template_file:
        markdown = markdown_file.read()
        template = template_file.read()
        html_string = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        template = re.sub(r"(\{\{ Title \}\})", title, template)
        template = re.sub(r"(\{\{ Content \}\})", html_string, template)
        markdown_file.close()
        template_file.close()
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as destination_file:
        destination_file.write(template)

def generate_pages(from_path:str, template_path:str, dest_path:str):
    contents = os.listdir(from_path)
    for content in contents:
        content_path = os.path.join(from_path, content)
        public_path = os.path.join(dest_path, content)
        if os.path.isfile(content_path):
            generate_page(content_path, template_path, public_path)
        elif os.path.isdir(content_path):
            generate_pages(content_path, template_path, public_path)
            

def main():
    copy_content("./static", "./public")
    generate_pages("./content", "./template.html", "./public")
    


main()