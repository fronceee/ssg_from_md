from htmlnode import LeafNode
from enums import TextType

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.Text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.Bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.Italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.Code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.Link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.Image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Invalid text type")

