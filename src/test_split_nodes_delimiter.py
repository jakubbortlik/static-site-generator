import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_missing_delimiter(self):
        input_node = TextNode("`bad example of code markdown", TextType.TEXT)
        self.assertRaises(
            ValueError, split_nodes_delimiter, [input_node], "`", TextType.CODE
        )
        input_node = TextNode("This is bad `example of code markdown", TextType.TEXT)
        self.assertRaises(
            ValueError, split_nodes_delimiter, [input_node], "`", TextType.CODE
        )
        input_node = TextNode(
            "This is another bad `example` of `code markdown", TextType.TEXT
        )
        self.assertRaises(
            ValueError, split_nodes_delimiter, [input_node], "`", TextType.CODE
        )

    def test_code_text_type(self):
        input_node = TextNode(
            "In Bash, use the `echo` command to print a message to the console.",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("In Bash, use the ", TextType.TEXT),
            TextNode("echo", TextType.CODE),
            TextNode(" command to print a message to the console.", TextType.TEXT),
        ]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "`", TextType.CODE)
        )

    def test_initial_code(self):
        input_node = TextNode(
            "`echo` is the Bash command to print a message to the console.",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("echo", TextType.CODE),
            TextNode(
                " is the Bash command to print a message to the console.", TextType.TEXT
            ),
        ]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "`", TextType.CODE)
        )

    def test_final_code(self):
        input_node = TextNode(
            "To print a message to the console in Bash use `echo`", TextType.TEXT
        )
        expected_nodes = [
            TextNode("To print a message to the console in Bash use ", TextType.TEXT),
            TextNode("echo", TextType.CODE),
        ]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "`", TextType.CODE)
        )

    def test_non_text_node(self):
        input_node = TextNode("echo", TextType.CODE)
        expected_nodes = [TextNode("echo", TextType.CODE)]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "`", TextType.CODE)
        )

    def test_consecutive_code_nodes(self):
        input_node = TextNode("Use the command `echo`` 'hello world'`.", TextType.TEXT)
        expected_nodes = [
            TextNode("Use the command ", TextType.TEXT),
            TextNode("echo", TextType.CODE),
            TextNode(" 'hello world'", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "`", TextType.CODE)
        )

    def test_bold_text_type(self):
        input_node = TextNode(
            "The following word **is** bold.",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("The following word ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" bold.", TextType.TEXT),
        ]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "**", TextType.BOLD)
        )

    def test_italic_text_type(self):
        input_node = TextNode(
            "The following word *is* italic.",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("The following word ", TextType.TEXT),
            TextNode("is", TextType.ITALIC),
            TextNode(" italic.", TextType.TEXT),
        ]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "*", TextType.ITALIC)
        )

    def test_multiword_italic_text_type(self):
        input_node = TextNode(
            "The following *words are* italic.",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("The following ", TextType.TEXT),
            TextNode("words are", TextType.ITALIC),
            TextNode(" italic.", TextType.TEXT),
        ]
        self.assertListEqual(
            expected_nodes, split_nodes_delimiter([input_node], "*", TextType.ITALIC)
        )

    def test_several_text_types(self):
        input_node = TextNode(
            "This is **bold**, and this is *italic*.",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", and this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(
            expected_nodes,
            split_nodes_delimiter(
                split_nodes_delimiter([input_node], "**", TextType.BOLD),
                "*",
                TextType.ITALIC,
            ),
        )
