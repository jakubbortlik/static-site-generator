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


def split_nodes_link(old_nodes) -> list[TextNode]:
    return split_nodes_by_element(old_nodes, links_regex, TextType.LINK)


def split_nodes_image(old_nodes) -> list[TextNode]:
    return split_nodes_by_element(old_nodes, images_regex, TextType.IMAGE)


def split_nodes_by_element(old_nodes, regex_, text_type) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        split_text = regex_.split(node.text)
        if len(node.text) == 0:
            continue
        if len(split_text) == 1:
            result.append(node)
            continue
        split_text_iter = iter(split_text)
        for part in split_text_iter:
            if part:
                result.append(TextNode(part, TextType.TEXT))
            try:
                alt_text = next(split_text_iter)
                url = next(split_text_iter)
            except StopIteration:
                continue
            result.append(TextNode(alt_text, text_type, url))
    return result


def text_to_textnodes(text) -> list[TextNode]:
    result = [TextNode(text, TextType.TEXT)]
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "*", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    return result
