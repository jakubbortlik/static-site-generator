import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_heading_paragraph_list(self):
        input_markdown = """# This is a heading

This is a paragraph. It has some **bold** and *italic* words inside of it.

* First list item in a list block
* This is a list item
* Yet another list item
"""
        self.assertListEqual(
            markdown_to_blocks(input_markdown),
            [
                "# This is a heading",
                "This is a paragraph. It has some **bold** and *italic* words inside of it.",
                "* First list item in a list block\n* This is a list item\n* Yet another list item",
            ],
        )

    def test_excessive_new_lines(self):
        input_markdown = """
This is a paragraph.


This is another paragraph.



This is yet another paragraph.
"""
        self.assertListEqual(
            markdown_to_blocks(input_markdown),
            ["This is a paragraph.", "This is another paragraph.",  "This is yet another paragraph."],
        )
