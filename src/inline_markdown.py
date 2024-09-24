from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    """Split TextType.TEXT nodes according to the delimiter."""
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Missing closing delimiter {delimiter}.")
        split_text_iter = iter(split_text)
        for part in split_text_iter:
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            try:
                special_node = next(split_text_iter)
            except StopIteration:
                continue
            new_nodes.append(TextNode(special_node, text_type))
    return new_nodes
