import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
class TestParentNode(unittest.TestCase):
    def test_to_html(self):

        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        node = ParentNode(None, [child1, child2], {"class": "greeting"})
        with self.assertRaises(ValueError):
            node.to_html()

        node = ParentNode("div", None, {"class": "greeting"})
        with self.assertRaises(ValueError):
            node.to_html()

        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        node = ParentNode("div", [child1, child2], {"class": "greeting"})
        expected_html = '<div class="greeting"><p>Hello, world!</p><a href="https://boot.dev">Click me!</a></div>'
        self.assertEqual(node.to_html(), expected_html)

        node = ParentNode("div", [child1, child2], None)
        expected_html = '<div><p>Hello, world!</p><a href="https://boot.dev">Click me!</a></div>'
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()