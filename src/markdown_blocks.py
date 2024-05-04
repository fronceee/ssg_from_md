from enums import BlockType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import os

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    hashtag_count = markdown_block.count("#")
    if hashtag_count > 0 and hashtag_count < 7:
        return BlockType.Heading
    if len(lines) > 0 and markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.Code
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.Paragraph
        return BlockType.Quote
    if markdown_block.startswith("* ") or markdown_block.startswith("- "):
        for line in lines:
            if not (line.startswith("* ") or line.startswith("- ")):
                return BlockType.Paragraph
        return BlockType.UnorderedList
    if markdown_block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return BlockType.Paragraph
        return BlockType.OrderList
    return BlockType.Paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def convert_to_heading_html_node(markdown_block):
    hashtag_count = markdown_block.count("#")
    if hashtag_count < 1 or hashtag_count > 6:
        raise ValueError("Invalid heading")
    children = text_to_children(markdown_block[hashtag_count+1:])
    return ParentNode(f"h{hashtag_count}", children, None)

def convert_to_code_html_node(markdown_block):
    if not markdown_block.startswith("```") or not markdown_block.endswith("```"):
        raise ValueError("Invalid code block")
    text = markdown_block[4:-3].strip()
    children = text_to_children(text)
    code = ParentNode("code", children,None)
    return ParentNode("pre", [code], None)

def convert_to_quote_html_node(markdown_block):
    lines = markdown_block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.strip(">").strip())
        
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children, None)

def convert_to_ul_html(markdown_block):
    lines = markdown_block.split("\n")
    childrens = []
    for line in lines:
        children = text_to_children(line[2:])
        childrens.append(ParentNode("li", children, None))
    return ParentNode("ul",childrens, None)

def convert_to_ol_html(markdown_block):
    lines = markdown_block.split("\n")
    childrens = []
    for line in lines:
        children = text_to_children(line[3:])
        childrens.append(ParentNode("li", children, None))
    return ParentNode("ol",childrens,None)

def convert_to_paragraph_html(markdown_block):
    lines = markdown_block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children, None)
    
def markdown_to_html_node(markdown):
    markdown_lines = markdown_to_blocks(markdown)
    childrens = []
    for line in markdown_lines:
        block_type_children = block_to_block_type(line)
        if block_type_children == BlockType.Heading:
            childrens.append(convert_to_heading_html_node(line))
            continue
        if block_type_children == BlockType.Code:
            childrens.append(convert_to_code_html_node(line))
            continue
        if block_type_children == BlockType.Quote:  
            childrens.append(convert_to_quote_html_node(line))
            continue
        if block_type_children == BlockType.UnorderedList:  
            childrens.append(convert_to_ul_html(line))
            continue 
        if block_type_children == BlockType.OrderList:
            childrens.append(convert_to_ol_html(line))
            continue
        if block_type_children == BlockType.Paragraph:
            childrens.append(convert_to_paragraph_html(line))
            continue
        raise ValueError("Invalid block type")
        
    return ParentNode("div",childrens, None)