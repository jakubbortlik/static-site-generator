import os

from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as in_file:
        markdown = in_file.read()
    with open(template_path)as in_file:
        template = in_file.read()
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    
    head, tail = os.path.split(dest_path)
    os.makedirs(head, exist_ok=True)
    with open(dest_path, "w") as out_file:
        out_file.write(template)
