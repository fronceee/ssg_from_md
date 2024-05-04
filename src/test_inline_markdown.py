import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import TextNode

from enums import TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.Text),
                TextNode("bolded", TextType.Bold),
                TextNode(" word", TextType.Text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.Text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.Text),
                TextNode("bolded", TextType.Bold),
                TextNode(" word and ", TextType.Text),
                TextNode("another", TextType.Bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.Text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.Text),
                TextNode("bolded word", TextType.Bold),
                TextNode(" and ", TextType.Text),
                TextNode("another", TextType.Bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "*", TextType.Italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.Text),
                TextNode("italic", TextType.Italic),
                TextNode(" word", TextType.Text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.Code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.Text),
                TextNode("code block", TextType.Code),
                TextNode(" word", TextType.Text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        )
        self.assertListEqual([("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.Text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.Text),
                TextNode("image", TextType.Image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.Text),
                TextNode(
                    "second image", TextType.Image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.Text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.Text),
                TextNode("link", TextType.Link, "https://boot.dev"),
                TextNode(" and ", TextType.Text),
                TextNode("another link", TextType.Link, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.Text),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.Text),
                TextNode("text", TextType.Bold),
                TextNode(" with an ", TextType.Text),
                TextNode("italic", TextType.Italic),
                TextNode(" word and a ", TextType.Text),
                TextNode("code block", TextType.Code),
                TextNode(" and an ", TextType.Text),
                TextNode("image", TextType.Image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.Text),
                TextNode("link", TextType.Link, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_text_only(self):
        nodes = text_to_textnodes(
            "This is text and i have no special formatting"
        )
        self.assertListEqual(
            [
                TextNode("This is text and i have no special formatting", TextType.Text),
            ],
            nodes,
        )
        
    def test_text_to_textnodes_empty_text(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)

    def test_text_to_textnodes_single_bold_word(self):
        nodes = text_to_textnodes("**bold**")
        self.assertListEqual([TextNode("bold", TextType.Bold)], nodes)

    def test_text_to_textnodes_single_italic_word(self):
        nodes = text_to_textnodes("*italic*")
        self.assertListEqual([TextNode("italic", TextType.Italic)], nodes)

    def test_text_to_textnodes_single_code_block(self):
        nodes = text_to_textnodes("`code block`")
        self.assertListEqual([TextNode("code block", TextType.Code)], nodes)

    def test_text_to_textnodes_single_image(self):
        nodes = text_to_textnodes("![image](https://example.com/image.png)")
        self.assertListEqual([TextNode("image", TextType.Image, "https://example.com/image.png")], nodes)

    def test_text_to_textnodes_single_link(self):
        nodes = text_to_textnodes("[link](https://example.com)")
        self.assertListEqual([TextNode("link", TextType.Link, "https://example.com")], nodes)

    def test_text_to_textnodes_multiple_formats(self):
        nodes = text_to_textnodes("This is **bold** and *italic* with a `code block` and an ![image](https://example.com/image.png) and a [link](https://example.com)")
        expected_nodes = [
            TextNode("This is ", TextType.Text),
            TextNode("bold", TextType.Bold),
            TextNode(" and ", TextType.Text),
            TextNode("italic", TextType.Italic),
            TextNode(" with a ", TextType.Text),
            TextNode("code block", TextType.Code),
            TextNode(" and an ", TextType.Text),
            TextNode("image", TextType.Image, "https://example.com/image.png"),
            TextNode(" and a ", TextType.Text),
            TextNode("link", TextType.Link, "https://example.com"),
        ]
        self.assertListEqual(expected_nodes, nodes)
    
if __name__ == "__main__":
    unittest.main()