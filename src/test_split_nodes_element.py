import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_link, split_nodes_image


class TestSplitNodesLink(unittest.TestCase):
    def test_no_link(self):
        node = TextNode(
            "There is no link in this node",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [TextNode("There is no link in this node", TextType.TEXT)],
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [],
        )

    def test_invalid_link(self):
        node = TextNode("[only link](https://www.boot.dev", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [TextNode("[only link](https://www.boot.dev", TextType.TEXT)],
        )

    def test_exiting_link_node(self):
        node = TextNode("This node is already an image", TextType.LINK, "https://url.com")
        self.assertListEqual(
            split_nodes_link([node]),
            [TextNode("This node is already an image", TextType.LINK, "https://url.com")],
        )

    def test_two_links(self):
        node = TextNode(
            "This is text with an image [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_two_links_without_other_text(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_only_link(self):
        node = TextNode("[only link](https://www.boot.dev)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [TextNode("only link", TextType.LINK, "https://www.boot.dev")],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_no_image(self):
        node = TextNode(
            "There is no image in this node",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("There is no image in this node", TextType.TEXT)],
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [],
        )

    def test_invalid_image(self):
        node = TextNode("![only image](https://www.boot.dev", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("![only image](https://www.boot.dev", TextType.TEXT)],
        )

    def test_exiting_image_node(self):
        node = TextNode("This node is already an image", TextType.IMAGE, "https://url.com")
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("This node is already an image", TextType.IMAGE, "https://url.com")],
        )

    def test_two_images(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_two_images_without_other_text(self):
        node = TextNode(
            "![image of boot](https://boot.jpg)![and of youtube](https://youtube.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("image of boot", TextType.IMAGE, "https://boot.jpg"),
                TextNode(
                    "and of youtube", TextType.IMAGE, "https://youtube.png"
                ),
            ],
        )

    def test_only_image(self):
        node = TextNode("![only image](https://www.boot.dev)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("only image", TextType.IMAGE, "https://www.boot.dev")],
        )

if __name__ == "__main__":
    unittest.main()
