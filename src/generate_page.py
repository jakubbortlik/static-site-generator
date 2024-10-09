import os

from markdown_to_html_node import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> None:
    for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(from_path):
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path) -> None:
    with open(from_path) as in_file:
        markdown = in_file.read()
    with open(template_path)as in_file:
        template = in_file.read()
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    
    dest_dir_path, tail = os.path.split(dest_path)
    if dest_dir_path != "":
        dest_path = os.path.splitext(dest_path)[0] + ".html"
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as out_file:
        out_file.write(template)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        num_sign, text = line.split(" ", maxsplit=1)
        if num_sign == "#":
            return text.strip()
    raise ValueError("No title in markdown")
