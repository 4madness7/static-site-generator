import unittest

from block_markdown import (
        markdown_to_blocks,
        block_to_block_type,
        markdown_to_html_node,
        extract_title
    )

class TestBlocks(unittest.TestCase):
    def test_md_to_blocks(self):
        test_string = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        result = markdown_to_blocks(test_string)
        expected = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        self.assertEqual(result, expected)

    def test_block_to_paragraph(self):
        block = "test\nnew line\n> not a quote\n# not a heading"
        res = block_to_block_type(block)
        self.assertEqual("paragraph", res)

    def test_block_to_unordered_list1(self):
        block = "- test\n- new line\n- not a quote\n- not a heading"
        res = block_to_block_type(block)
        self.assertEqual("unordered_list", res)

    def test_block_to_unordered_list2(self):
        block = "* test\n- new line\n- not a quote\n- not a heading"
        res = block_to_block_type(block)
        self.assertNotEqual("unordered_list", res)

    def test_block_to_ordered_list(self):
        block = "1. test\n2. new line\n3. nothing"
        res = block_to_block_type(block)
        self.assertEqual("ordered_list", res)

    def test_block_to_code(self):
        block = "```\ntest\nnew line\nnothing\n```"
        res = block_to_block_type(block)
        self.assertEqual("code", res)

    def test_block_to_wrong_code(self):
        block = "``\ntest\nnew line\nnothing\n```"
        res = block_to_block_type(block)
        self.assertNotEqual("code", res)

    def test_block_to_quote(self):
        block = ">test\n>new line\n>nothing"
        res = block_to_block_type(block)
        self.assertEqual("quote", res)

    def test_block_to_heading(self):
        block = "### test"
        res = block_to_block_type(block)
        self.assertEqual("heading", res)

    def test_md_to_html(self):
        md1 = """### heading

```
this is a code block
```

> quote,
> a very *nice* one

- item *test*
- item2

1. item *test*
2. item2

this is a paragraph
this is **bold** to say"""

        md2 = """## heading

```
this is a code block
```

> quote,
> a very *nice* one

- item *test*
- item2

1. item *test*
2. item2

this is a paragraph
this is **bold** to say"""
        res1 = markdown_to_html_node(md1)
        res2 = markdown_to_html_node(md2)
        self.assertNotEqual(res1, res2)

    def test_extract_title(self):
        res = extract_title("# Title")
        expected = "Title"
        self.assertEqual(res, expected)

    def test_extract_title_mismatch(self):
        res = extract_title("# New Title")
        expected = "Title"
        self.assertNotEqual(res, expected)

if __name__ == "__main__":
    unittest.main()
