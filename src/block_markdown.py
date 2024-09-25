def markdown_to_blocks(markdown) -> list[str]:
    return list(filter(lambda x: len(x) > 0, map(str.strip, markdown.split("\n\n"))))
