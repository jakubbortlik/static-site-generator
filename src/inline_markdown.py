import re

from textnode import TextNode, TextType

images_regex = re.compile(r"!\[(.*?)\]\((.*?)\)")
links_regex = re.compile(r"(?<!!)\[(.*?)\]\((.*?)\)")


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    """Split TextType.TEXT nodes according to the delimiter."""
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Missing closing delimiter {delimiter}.")
        split_text_iter = iter(split_text)
        for part in split_text_iter:
            if part:
                result.append(TextNode(part, TextType.TEXT))
            try:
                special_node = next(split_text_iter)
            except StopIteration:
                continue
            result.append(TextNode(special_node, text_type))
    return result


def extract_markdown_images(text) -> list[tuple[str, ...]]:
    return images_regex.findall(text)


def extract_markdown_links(text) -> list[tuple[str, ...]]:
    return links_regex.findall(text)
