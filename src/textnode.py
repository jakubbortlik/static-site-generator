from htmlnode import LeafNode

import enum


class TextType(enum.StrEnum):
    TEXT = enum.auto()
    BOLD = enum.auto()
    ITALIC = enum.auto()
    CODE = enum.auto()
    LINK = enum.auto()
    IMAGE = enum.auto()


class TextNode:
    def __init__(self, text: str, text_type: str, url: str | None = None) -> None:
        """Initialize a text node.

        Args:
            text: The text content of the node.
            text_type: The type of text this node contains, e.g., "bold", "italic".
            url: The URL of the link or image, if the text is a link.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f'TextNode("{self.text}", "{self.text_type}", "{self.url}")'


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}.")
