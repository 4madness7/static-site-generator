from textnode import *
import os
import shutil
from block_markdown import markdown_to_html_node, extract_title

def main():
    prepare_public_dir()
    generate_pages_recursive("content", "template.html", "public")

def prepare_public_dir():
    dir = "./public"
    if not os.path.exists(dir):
        os.mkdir(dir)
    print("=== Start: Deleting ./public directory. ===")
    for filename in os.listdir(dir):
        complete = os.path.join(dir, filename)
        if os.path.isfile(complete):
            os.unlink(complete)
        else:
            shutil.rmtree(complete)
    print("=== Finished: Deleting ./public directory. ===")
    print("=== Start: Copying ./static contents in ./public directory. ===")
    recursive_file_copy("./static", dir)
    print("=== Finished: Copying ./static contents in ./public directory. ===")

def recursive_file_copy(from_dir, to_dir):
    for content in os.listdir(from_dir):
        full_from_dir = os.path.join(from_dir, content)
        full_to_dir = os.path.join(to_dir, content)
        if os.path.isdir(full_from_dir):
            os.mkdir(full_to_dir)
            print(f"=== Creating {full_to_dir} directory. ===")
            recursive_file_copy(full_from_dir, full_to_dir)
        else:
            shutil.copy(full_from_dir, full_to_dir)
            print(f"=== Copying {full_from_dir} to {full_to_dir}. ===")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"=== Start: Generating page from {dir_path_content} to {dest_dir_path} using {template_path} ===")

    for dir_list in os.listdir(dir_path_content):
        full_from_dir = os.path.join(dir_path_content, dir_list)
        full_to_dir = os.path.join(dest_dir_path, dir_list)
        if os.path.isdir(full_from_dir):
            os.mkdir(full_to_dir)
            print(f"=== Creating {full_to_dir} directory. ===")
            generate_pages_recursive(full_from_dir, template_path ,full_to_dir)
        else:
            from_file = open(full_from_dir, "r")
            from_file_content = from_file.read()
            from_file.close()

            template_file = open(template_path, "r")
            template_file_content = template_file.read()
            template_file.close()

            html_title = extract_title(from_file_content)
            html_content = markdown_to_html_node(from_file_content).to_html()

            dest_html = template_file_content.replace("{{ Title }}", html_title)
            dest_html = dest_html.replace("{{ Content }}", html_content)

            dest_file_path = os.path.join(dest_dir_path, "index.html")
            dest_file = open(dest_file_path, "w")
            dest_file.write(dest_html)
            dest_file.close()

    print(f"=== Finished: Generating page from {dir_path_content} to {dest_dir_path} using {template_path} ===")


if __name__ == "__main__":
    main()
