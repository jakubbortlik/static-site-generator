import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://manjaro.org"})
        self.assertEqual(node.props_to_html(), ' href="https://manjaro.org"')

    def test_props_to_html_2_args(self):
        node = HTMLNode(props={"href": "https://manjaro.org", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://manjaro.org" target="_blank"'
        )

    def test_props_to_html_None_args(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_0_args(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_to_html_without_value(self):
        leaf_node = LeafNode(tag=None, value=None)
        self.assertRaises(ValueError, leaf_node.to_html)

    def test_to_html_without_tag(self):
        leaf_node = LeafNode(tag=None, value="This is some raw text")
        self.assertEqual(leaf_node.to_html(), "This is some raw text")

    def test_to_html_with_empty_tag(self):
        leaf_node2 = LeafNode(tag="", value="This is some raw text")
        self.assertEqual(leaf_node2.to_html(), "This is some raw text")

    def test_to_html_Boolean_value_without_tag(self):
        leaf_node = LeafNode(tag=None, value=True)
        self.assertEqual(leaf_node.to_html(), "True")

    def test_to_html_list_value_without_tag(self):
        leaf_node2 = LeafNode(tag="", value=["Hello", "world"])
        self.assertEqual(leaf_node2.to_html(), "['Hello', 'world']")

    def test_to_html_with_tag(self):
        leaf_node = LeafNode(
            value="This is some raw text",
            tag="p",
        )
        self.assertEqual(leaf_node.to_html(), "<p>This is some raw text</p>")

    def test_to_html_with_tag_and_props(self):
        leaf_node = LeafNode(
            value="This is the link to manjaro.org",
            tag="a",
            props={"href": "https://manjaro.org"},
        )
        self.assertEqual(
            leaf_node.to_html(),
            '<a href="https://manjaro.org">This is the link to manjaro.org</a>',
        )


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        parent_node = ParentNode(
            tag=None,
            value=None,
            children=[LeafNode("a", "node 1"), LeafNode("a", "node 2")],
        )
        self.assertRaises(ValueError, parent_node.to_html)

    def test_empty_tag(self):
        parent_node = ParentNode(
            tag="",
            value=None,
            children=[LeafNode("a", "node 1"), LeafNode("b", "node 2")],
        )
        self.assertRaises(ValueError, parent_node.to_html)

    def test_no_children(self):
        parent_node = ParentNode(tag="p", value=None, children=None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_empty_children(self):
        parent_node = ParentNode(tag="p", value=None, children=[])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_node_with_children(self):
        parent_node = ParentNode(
            "p",
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_node_with_nested_children(self):
        parent_node = ParentNode(
            "p",
            None,
            [
                ParentNode(
                    "ul",
                    value=None,
                    children=[LeafNode("li", "Item 1"), LeafNode("li", "Item 2")],
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><ul><li>Item 1</li><li>Item 2</li></ul>Normal text</p>",
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_raw_text(self):
        text = "this is raw text"
        text_node = TextNode(text=text, text_type="text")
        leaf_node = LeafNode(tag=None, value=text)
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_bold_text(self):
        text = "this is bold text"
        text_node = TextNode(text=text, text_type="bold")
        leaf_node = LeafNode(tag="b", value=text)
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_italic_text(self):
        text = "this is italic text"
        text_node = TextNode(text=text, text_type="italic")
        leaf_node = LeafNode(tag="i", value=text)
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_code_text(self):
        text = "this is code text"
        text_node = TextNode(text=text, text_type="code")
        leaf_node = LeafNode(tag="code", value=text)
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_link(self):
        text = "this is an image"
        url = "https://link.com"
        text_node = TextNode(text=text, text_type="link", url=url)
        leaf_node = LeafNode(tag="a", value=text, props={"href": url})
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_image(self):
        text = "this is an image"
        url = "https://link.com"
        text_node = TextNode(text=text, text_type="image", url=url)
        leaf_node = LeafNode(tag="img", value="", props={"src": url, "alt": text})
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_unsupported_text_type(self):
        text_node = TextNode(text="some text", text_type="unsupported")
        self.assertRaises(ValueError, text_node_to_html_node, text_node)


if __name__ == "__main__":
    unittest.main()
