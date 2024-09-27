import enum 
import re

heading_regex = re.compile("^#{1,6} .*$")


class BlockType(enum.StrEnum):
    PARAGRAPH = enum.auto()
    HEADING = enum.auto()
    CODE = enum.auto()
    QUOTE = enum.auto()
    UNORDERED_LIST = enum.auto()
    ORDERED_LIST = enum.auto()


def markdown_to_blocks(markdown) -> list[str]:
    return list(filter(lambda x: len(x) > 0, map(str.strip, markdown.split("\n\n"))))


def block_to_block_type(markdown_block) -> BlockType:
    block_lines = markdown_block.split("\n")
    if heading_regex.match(markdown_block):
        return BlockType.HEADING
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block_lines):
        return BlockType.QUOTE
    if all(line.startswith("* ") or line.startswith("- ") for line in block_lines):
        return BlockType.UNORDERED_LIST
    for i, line in enumerate(block_lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
