import re

from enums import TextType
from textnode import TextNode, text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.Text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.Text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes



def extract_markdown_images(text):
    patterns = r"!\[(.*?)\]\((.*?)\)"
    img_links = re.findall(patterns, text)
    return img_links

def extract_markdown_links(text):  
    patterns = r"\[(.*?)\]\((.*?)\)"
    links = re.findall(patterns, text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.Text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if not images:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid Markdown syntax, image not found")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], old_node.text_type))
            new_nodes.append(TextNode(image[0], TextType.Image, image[1]))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, old_node.text_type))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.Text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if not links:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid Markdown syntax, link not found")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], old_node.text_type))
            new_nodes.append(TextNode(link[0], TextType.Link, link[1]))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, old_node.text_type))
    return new_nodes

def print_nodes(nodes):
    print("[")
    for node in nodes:
        print(node, ",")
    print("]")
    print("--------------------------------")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.Text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.Bold)
    nodes = split_nodes_delimiter(nodes, "*", TextType.Italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.Code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

# nodes = text_to_textnodes("![image](https://example.com/image.png)")
    
# text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)")