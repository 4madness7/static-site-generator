import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_match(self):
        node = HTMLNode(props={"href":"boot.dev"})
        expected = ' href="boot.dev"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_mismatch(self):
        node = HTMLNode(props={"href":"boot.dev", "target": "__blank"})
        expected = 'href="boot.dev"'
        self.assertNotEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode(tag="p", value="Backend is so cool!", props={"href":"boot.dev", "target": "__blank"})
        expected = ("HTMLNode(\n" +
                      "\ttag = p\n" +
                      "\tvalue = Backend is so cool!\n" +
                      "\tchildren = None\n" +
                      "\tprops = {'href': 'boot.dev', 'target': '__blank'}\n" +
                   ")"
                )
        self.assertEqual(expected, repr(node))

class TestLeafNode(unittest.TestCase):
    def test_to_html_match_1(self):
        node = LeafNode(tag="p", value="this is so cool")
        expected = "<p>this is so cool</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_match_2(self):
        node = LeafNode(tag="a",value="this is so cool", props={"href":"boot.dev"})
        expected = '<a href="boot.dev">this is so cool</a>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_mismatch(self):
        node = LeafNode(value="this is so cool", tag="p")
        expected = 'this is so cool'
        self.assertNotEqual(node.to_html(), expected)

    def test_repr(self):
        node = LeafNode(tag="p", value="Backend is so cool!", props={"href":"boot.dev", "target": "__blank"})
        expected = ("LeafNode(\n" +
                      "\ttag = p\n" +
                      "\tvalue = Backend is so cool!\n" +
                      "\tprops = {'href': 'boot.dev', 'target': '__blank'}\n" +
                   ")"
                )
        self.assertEqual(expected, repr(node))

class TestParentNode(unittest.TestCase):
    def test_to_html_match_1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_match_2(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                    props = {"class": "primary"}
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><p class=\"primary\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

class TestTextToHTMLConverion(unittest.TestCase):
    def test_bold(self):
        node = text_node_to_html_node(TextNode("test", TextType.BOLD))
        expected = LeafNode("b", "test")
        self.assertEqual(node, expected)

    def test_italic(self):
        node = text_node_to_html_node(TextNode("test", TextType.ITALIC))
        expected = LeafNode("i", "test")
        self.assertEqual(node, expected)

    def test_code(self):
        node = text_node_to_html_node(TextNode("test", TextType.CODE))
        expected = LeafNode("code", "test")
        self.assertEqual(node, expected)

    def test_links(self):
        node = text_node_to_html_node(TextNode("test", TextType.LINK, "boot.dev"))
        expected = LeafNode("a", "test", {"href": "boot.dev"})
        self.assertEqual(node, expected)

    def test_images(self):
        node = text_node_to_html_node(TextNode("test", TextType.IMAGE, "test.png"))
        expected = LeafNode("img", "", {"src": "test.png", "alt": "test"})
        self.assertEqual(node, expected)


if __name__ == "__main__":
    unittest.main()
