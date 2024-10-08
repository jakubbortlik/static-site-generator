def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        num_sign, text = line.split(" ", maxsplit=1)
        if num_sign == "#":
            return text.strip()
    raise ValueError("No title in markdown")
