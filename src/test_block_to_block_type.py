import unittest

from block_markdown import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a simple paragraph.\nWith two lines, actually."
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_headings(self):
        markdown = "# This is a simple heading"
        self.assertEqual(block_to_block_type(markdown), BlockType.HEADING)
        markdown = "## This is a second-order heading"
        self.assertEqual(block_to_block_type(markdown), BlockType.HEADING)
        markdown = "####### This is a paragraph with 7 # characters"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "# This is a paragraph starting with a # character\n# in every line."
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        markdown = "```print(i)```"
        self.assertEqual(block_to_block_type(markdown), BlockType.CODE)
        markdown = "```print(i)\n```"
        self.assertEqual(block_to_block_type(markdown), BlockType.CODE)
        markdown = "```for i in range(10):\n    print(i)```"
        self.assertEqual(block_to_block_type(markdown), BlockType.CODE)

    def test_quotes(self):
        markdown = "> some quoted text"
        self.assertEqual(block_to_block_type(markdown), BlockType.QUOTE)
        markdown = ">some more quoted text"
        self.assertEqual(block_to_block_type(markdown), BlockType.QUOTE)

    def test_unordered_list(self):
        markdown = "* list item"
        self.assertEqual(block_to_block_type(markdown), BlockType.UNORDERED_LIST)
        markdown = "- list item"
        self.assertEqual(block_to_block_type(markdown), BlockType.UNORDERED_LIST)
        markdown = "- list item\n* another item"
        self.assertEqual(block_to_block_type(markdown), BlockType.UNORDERED_LIST)
        markdown = "- list item\n* another item\nnot a list item"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        markdown = "1. first list item"
        self.assertEqual(block_to_block_type(markdown), BlockType.ORDERED_LIST)
        markdown = "1. first list item\n2. second list item"
        self.assertEqual(block_to_block_type(markdown), BlockType.ORDERED_LIST)
        markdown = "0. ordered list must start at 1!"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "1. first list item\n3. second list item must be number 2"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "1. first list item\nevery item must be numbered"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "1.there must be a space after the number"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
