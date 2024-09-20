from htmlnode import LeafNode


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
        case "text":
            return LeafNode(tag=None, value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case "image":
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}.")
