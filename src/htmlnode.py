from collections.abc import Sequence

class HTMLNode():
    def __init__(self, tag:str| None = None, 
                 value:str | None = None, 
                 children:Sequence[HTMLNode] | None = None, 
                 props:dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        output = ""
        if self.props == None:
            return None
        for prop in self.props:
            output += f' {prop}="{self.props[prop]}"'
        return output

    def __repr__(self) -> str:
        return f"HTMLNode: ({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other: HTMLNode) -> bool:
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str| None, value: str, props: dict | None = None) -> None:
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("value cannot be empty")
        elif self.tag == None:
            return str(self.value)
        else:
            return f'<{self.tag}{self.props_to_html() if self.props_to_html() != None else ""}>{self.value}</{self.tag}>'
        
    def __repr__(self) -> str:
        return f"HTMLNode: ({self.tag}, {self.value}, {self.props})"
        
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: Sequence[HTMLNode], props: dict | None = None) -> None:
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag == None:
            raise ValueError("tag couldn't be empty")
        elif self.children == None:
            raise ValueError("children couldn't be empty")
        else:
            child_text = ""
            for child in self.children:
                child_text += child.to_html()
            return f'<{self.tag}{self.props_to_html() if self.props_to_html() != None else ""}>{child_text}</{self.tag}>'
        
            