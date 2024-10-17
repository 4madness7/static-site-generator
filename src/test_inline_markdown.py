import unittest

from textnode import TextType, TextNode
from inline_markdown import (
        split_nodes_delimiter,
        extract_markdown_links,
        extract_markdown_images,
        split_nodes_link,
        split_nodes_image,
        text_to_textnodes
    )

class TestMDtoHTML(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is **bold** node", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold2(self):
        node = TextNode("**This is** bold node", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
                TextNode("This is", TextType.BOLD),
                TextNode(" bold node", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic(self):
        node = TextNode("This is *italic* node", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code(self):
        node = TextNode("This is `code` node", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold_multiword(self):
        node = TextNode("This is **bold** node **multiword**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" node ", TextType.TEXT),
                TextNode("multiword", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_italic_multiword(self):
        node = TextNode("This is *italic* node *multiword*", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" node ", TextType.TEXT),
                TextNode("multiword", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_code_multiword(self):
        node = TextNode("This is `code` node `multiword`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" node ", TextType.TEXT),
                TextNode("multiword", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_extract_link(self):
        result = extract_markdown_links("[link](boot.dev) and ![image](image.png)")
        expected = [ ("link", "boot.dev") ]
        self.assertEqual(result, expected)

    def test_extract_images(self):
        result = extract_markdown_images("[link](boot.dev) and ![image](image.png)")
        expected = [ ("image", "image.png") ]
        self.assertEqual(result, expected)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        res = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(res, expected)



if __name__ == "__main__":
    unittest.main()
