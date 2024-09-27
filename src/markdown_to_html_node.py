import re

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


unordered_list_prefix_regex = re.compile("^[*-] ")
ordered_list_prefix_regex = re.compile(r"^[0-9]+\. ")
quote_prefix_regex = re.compile("^> *")


def text_to_children(text) -> list[HTMLNode]:
    result: list[HTMLNode] = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        result.append(text_node_to_html_node(text_node))
    return result


def markdown_to_html_heading(markdown):
    heading_level, text = markdown.split(" ", maxsplit=1)
    return LeafNode(tag=f"h{len(heading_level)}", value=text)


def markdown_to_html_code(markdown):
    return ParentNode(
        tag="pre",
        value=None,
        children=[LeafNode(tag="code", value=markdown.strip("`").strip())],
    )


def markdown_to_html_unordered_list(markdown):
    lines = [unordered_list_prefix_regex.sub("", line) for line in markdown.split("\n")]
    return ParentNode(
        tag="ul",
        value=None,
        children=[
            ParentNode(tag="li", value=None, children=text_to_children(line))
            for line in lines
        ],
    )


def markdown_to_html_ordered_list(markdown):
    lines = [ordered_list_prefix_regex.sub("", line) for line in markdown.split("\n")]
    return ParentNode(
        tag="ol",
        value=None,
        children=[
            ParentNode(tag="li", value=None, children=text_to_children(line))
            for line in lines
        ],
    )


def lines_grouped_by_prefix(markdown) -> list[str]:
    result = []
    old_line_type = None
    for line in (quote_prefix_regex.sub("", line) for line in markdown.split("\n")):
        line_type = "QUOTE" if line.startswith(">") else "NO_QUOTE"
        if not line_type == old_line_type:
            result.append(line)
            old_line_type = line_type
        else:
            result[-1] += "\n" + line
    return result


def markdown_to_html_quote(markdown) -> ParentNode:
    children = []
    for line_group in lines_grouped_by_prefix(markdown):
        if line_group.startswith(">"):
            children.append(markdown_to_html_quote(line_group))
        else:
            for block in markdown_to_blocks(line_group):
                children.append(
                    ParentNode(
                        tag="p", value=None, children=markdown_to_html_nodes(block)
                    )
                )
    return ParentNode(tag="blockquote", value=None, children=children)


def markdown_to_html_nodes(markdown) -> list[HTMLNode]:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children.extend(text_to_children(block))
        elif block_type == BlockType.HEADING:
            children.append(markdown_to_html_heading(block))
        elif block_type == BlockType.CODE:
            children.append(markdown_to_html_code(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(markdown_to_html_unordered_list(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(markdown_to_html_ordered_list(block))
        elif block_type == BlockType.QUOTE:
            children.append(markdown_to_html_quote(block))

    return children


def markdown_to_html_node(markdown) -> HTMLNode:
    children = markdown_to_html_nodes(markdown)
    result = ParentNode(tag="div", value=None, children=children, props=None)
    return result
