import unittest

from htmlnode import LeafNode, ParentNode
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_simple_paragraph(self):
        markdown = "This is a simple paragraph"
        self.assertEqual(
            markdown_to_html_node(markdown),
            ParentNode(
                tag="div",
                value=None,
                children=[LeafNode(tag=None, value="This is a simple paragraph")],
                props=None,
            ),
        )

    def test_paragraph_with_bold(self):
        markdown = "This is a simple paragraph with **bold text**."
        self.assertEqual(
            markdown_to_html_node(markdown),
            ParentNode(
                tag="div",
                value=None,
                children=[
                    LeafNode(tag=None, value="This is a simple paragraph with "),
                    LeafNode(tag="b", value="bold text"),
                    LeafNode(tag=None, value="."),
                ],
                props=None,
            ),
        )

    def test_heading(self):
        markdown = "# This is a simple heading"
        self.assertEqual(
            markdown_to_html_node(markdown),
            ParentNode(
                tag="div",
                value=None,
                children=[LeafNode(tag="h1", value="This is a simple heading")],
                props=None,
            ),
        )
        markdown = "## This is a second-level heading"
        self.assertEqual(
            markdown_to_html_node(markdown),
            ParentNode(
                tag="div",
                value=None,
                children=[LeafNode(tag="h2", value="This is a second-level heading")],
                props=None,
            ),
        )
        markdown = "####### This is NOT a seventh-level heading"
        self.assertEqual(
            markdown_to_html_node(markdown),
            ParentNode(
                tag="div",
                value=None,
                children=[
                    LeafNode(
                        tag=None, value="####### This is NOT a seventh-level heading"
                    )
                ],
                props=None,
            ),
        )

    def test_code_blocks(self):
        markdown = """```
for i in range(10):
    print(i)
```
"""
        self.assertEqual(
            markdown_to_html_node(markdown),
            ParentNode(
                tag="div",
                value=None,
                children=[
                    ParentNode(
                        tag="pre",
                        value=None,
                        children=[
                            LeafNode(
                                tag="code", value="for i in range(10):\n    print(i)"
                            )
                        ],
                    )
                ],
            ),
        )

    def test_unordered_list(self):
        markdown = "* first item\n* - second item with an extra hyphen"
        actual_value = markdown_to_html_node(markdown)
        expected_val = ParentNode(
            tag="div",
            value=None,
            children=[
                ParentNode(
                    tag="ul",
                    value=None,
                    children=[
                        ParentNode(
                            tag="li",
                            value=None,
                            children=[LeafNode(tag=None, value="first item")],
                        ),
                        ParentNode(
                            tag="li",
                            value=None,
                            children=[
                                LeafNode(
                                    tag=None, value="- second item with an extra hyphen"
                                )
                            ],
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(actual_value, expected_val)

    def test_ordered_list(self):
        markdown = "1. first item\n2. - second item with an extra hyphen"
        actual_value = markdown_to_html_node(markdown)
        expected_val = ParentNode(
            tag="div",
            value=None,
            children=[
                ParentNode(
                    tag="ol",
                    value=None,
                    children=[
                        ParentNode(
                            tag="li",
                            value=None,
                            children=[LeafNode(tag=None, value="first item")],
                        ),
                        ParentNode(
                            tag="li",
                            value=None,
                            children=[
                                LeafNode(
                                    tag=None, value="- second item with an extra hyphen"
                                )
                            ],
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(actual_value, expected_val)

    def test_quote(self):
        markdown = (
            ">first line is a *kind* of heading\n>\n>second line is a separate paragraph\n"
            ">spread over two lines\n>> third (nested) line\n"
            "> > > fourth (even more nested) line\n>fifth line"
        )
        actual_value = markdown_to_html_node(markdown)
        expected_val = ParentNode(
            tag="div",
            value=None,
            children=[
                ParentNode(
                    tag="blockquote",
                    value=None,
                    children=[
                        ParentNode(
                            tag="p",
                            value=None,
                            children=[
                                LeafNode(
                                    tag=None, value="first line is a "
                                ),
                                LeafNode(
                                    tag="i", value="kind"
                                ),
                                LeafNode(
                                    tag=None, value=" of heading"
                                ),
                            ],
                        ),
                        ParentNode(
                            tag="p",
                            value=None,
                            children=[
                                LeafNode(
                                    tag=None,
                                    value="second line is a separate paragraph\nspread over two lines",
                                )
                            ],
                        ),
                        ParentNode(
                            tag="blockquote",
                            value=None,
                            children=[
                                ParentNode(
                                    tag="p",
                                    value=None,
                                    children=[
                                        LeafNode(tag=None, value="third (nested) line")
                                    ],
                                ),
                                ParentNode(
                                    tag="blockquote",
                                    value=None,
                                    children=[
                                        ParentNode(
                                            tag="p",
                                            value=None,
                                            children=[
                                                LeafNode(
                                                    tag=None,
                                                    value="fourth (even more nested) line",
                                                )
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                        ParentNode(
                            tag="p",
                            value=None,
                            children=[LeafNode(tag=None, value="fifth line")],
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(actual_value, expected_val)


if __name__ == "__main__":
    unittest.main()
