from __future__ import annotations

from typing import Sequence


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        """Initialize an HTML node.

        Args:
            tag: The tag name, e.g., "p", "a", etc.
            value: The value of the HTML tag (e.g., the text inside a paragraph).
            children: The children of this node.
            props: The attributes of the HTML tag, e.g., {"href": "https://manjaro.org"}.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is not None:
            return "".join(f' {key}="{val}"' for key, val in self.props.items())
        return ""

    def __repr__(self):
        args = []
        if self.tag is not None:
            args.append(f'tag="{self.tag}"')
        if self.value is not None:
            args.append(f'value="{self.value}"')
        if self.children is not None:
            args.append(f"children={self.children}")
        if self.props is not None:
            args.append(f'props={self.props}')
        return f"{self.__class__.__name__}({', '.join(args)})"

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError(f"Leaf nodes must have a value, but it is {self.value}.")
        if self.tag is None or self.tag == "":
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        children: Sequence[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError(f"Parent nodes must have a tag, but it is {self.tag}.")
        if self.children is None or len(self.children) == 0:
            raise ValueError(
                f"Parent nodes must have children, but it is {self.children}."
            )
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
