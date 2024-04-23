import os
from pathlib import Path

from markdown_blocks import (
  markdown_to_blocks,  
  markdown_to_html_node
)

def open_and_read_file(file):
    obj = open(file)
    content = obj.read()
    obj.close()
    return content

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if blocks[0].startswith("# "):
        return blocks[0][2:]
    raise Exception("Markdown has no h1 header!")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    markdown_content = open_and_read_file(from_path)
    template_content = open_and_read_file(template_path)
    html_code = markdown_to_html_node(markdown_content).to_html()
    page_title = extract_title(markdown_content)
    template_content = template_content.replace('{{ Title }}', page_title)
    template_content = template_content.replace('{{ Content }}', html_code)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)   