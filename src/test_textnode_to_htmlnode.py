import unittest

from htmlnode import LeafNode
from textnode import TextNode, text_node_to_html_node


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
