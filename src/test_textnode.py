import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_no_url(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a link node", "bold", "/data/pictures")
        node2 = TextNode("This is a link node", "bold", "/data/pictures")
        self.assertEqual(node, node2)

    def test_eq_with_different_text_type(self):
        node = TextNode("This is an italic text node", "italic")
        node2 = TextNode("This is an italic text node", "italic")
        self.assertEqual(node, node2)

    def test_eq_with_empty_text_type(self):
        node = TextNode("This is a text node with no text type", "")
        node2 = TextNode("This is a text node with no text type", "")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a Text Node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a Text Node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a Text Node", "bold", "my/url")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
