import re
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def check_start_of_every_line(block, char):
    for line in block.split("\n"):
        if not line.startswith(char):
            return False
    return True

def check_ordered_list(block):
    i = 1
    for line in block.split("\n"):
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = filter(lambda b: b != "", blocks)
    blocks = map(lambda b: b.strip(), blocks)
    return list(blocks)

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    is_quote = check_start_of_every_line(block, ">")
    if is_quote:
        return "quote"
    is_ulist_astk = check_start_of_every_line(block, "* ")
    if is_ulist_astk:
        return "unordered_list"
    is_ulist_dash = check_start_of_every_line(block, "- ")
    if is_ulist_dash:
        return "unordered_list"
    is_olist = check_ordered_list(block)
    if is_olist:
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    first_html = ParentNode("div", [], None)
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                num = len(re.findall(r"#{1,6}", block)[0])
                heading_node = LeafNode(f"h{num}", block[num + 1:])
                first_html.children.append(heading_node)
            case "code":
                code_node = ParentNode("pre", [LeafNode("code", block[4:-3].strip())])
                first_html.children.append(code_node)
            case "quote":
                children = []
                for line in block.split("\n"):
                    nodes = text_to_textnodes(line[1:].strip())
                    for node in nodes:
                        html_node = text_node_to_html_node(node)
                        children.append(html_node)

                quote_node = ParentNode("blockquote", children)
                first_html.children.append(quote_node)
            case "unordered_list":
                children = []
                for line in block.split("\n"):
                    nodes = text_to_textnodes(line[2:])
                    child = ParentNode("li", [])
                    for node in nodes:
                        html_node = text_node_to_html_node(node)
                        child.children.append(html_node)
                    children.append(child)


                ul_node = ParentNode("ul", children)
                first_html.children.append(ul_node)
            case "ordered_list":
                children = []
                for line in block.split("\n"):
                    nodes = text_to_textnodes(line[2:].strip())
                    child = ParentNode("li", [])
                    for node in nodes:
                        html_node = text_node_to_html_node(node)
                        child.children.append(html_node)
                    children.append(child)
                ol_node = ParentNode("ol", children)
                first_html.children.append(ol_node)
            case "paragraph":
                children = []
                for line in block.split("\n"):
                    nodes = text_to_textnodes(line.strip())
                    for node in nodes:
                        html_node = text_node_to_html_node(node)
                        children.append(html_node)

                p_node = ParentNode("p", children)
                first_html.children.append(p_node)

    return first_html

def extract_title(markdown):
    lines = markdown.split("\n")
    if lines[0].strip().startswith("# "):
        return lines[0][2:].strip()
    raise Exception("File does not present a title, please add one in the first line.")
