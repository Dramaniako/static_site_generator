import os
import shutil
from textnode import TextNode, TextType

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


def main():
    copy_content("./static", "./public")


main()