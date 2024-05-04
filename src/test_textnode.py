import unittest
from enums import TextType
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Text)
        node2 = TextNode("This is a text node", TextType.Text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.Text)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.Text)
        node2 = TextNode("This is a text node2", TextType.Text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.Text, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.Text, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.Text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, (0,), https://www.boot.dev)", repr(node)
        )



if __name__ == "__main__":
    unittest.main()
