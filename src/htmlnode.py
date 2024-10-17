class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented yet")

    def props_to_html(self):
        props = ""
        if self.props is None:
            return props
        for k in self.props:
            props += f" {k}=\"{self.props[k]}\""
        return props

    def __repr__(self) -> str:
        return ("HTMLNode(\n" +
                      f"\ttag = {self.tag}\n" +
                      f"\tvalue = {self.value}\n" +
                      f"\tchildren = {self.children}\n" +
                      f"\tprops = {self.props}\n" +
                   ")"
                )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None ,props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )

    def __repr__(self) -> str:
        return ("LeafNode(\n" +
                      f"\ttag = {self.tag}\n" +
                      f"\tvalue = {self.value}\n" +
                      f"\tprops = {self.props}\n" +
                   ")"
                )


class ParentNode(HTMLNode):
    def __init__(self, tag ,children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must contain at least one child")
        content = ""
        for child in self.children:
            content += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"
