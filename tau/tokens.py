import typing


class Coord(typing.NamedTuple):
    col: int
    line: int

    def __str__(self):
        return f"{self.line}:{self.col}"

    def __repr__(self):
        return f"Coord({self.col}, {self.line})"


class Span(typing.NamedTuple):
    start: Coord
    end: Coord

    def __str__(self):
        return f"{self.start} - {self.end}"

    def __repr__(self):
        return f"Span({self.start.__repr__()}, {self.end.__repr__()})"


class Token(typing.NamedTuple):
    kind: str
    value: str
    span: Span

    def __repr__(self) -> str:
        return f"Token({self.kind.__repr__()}, {self.value.__repr__()}, {self.span.__repr__()})"


punctuation: list[str] = [
    ":",
    ",",
    "!=",
    "&",
    "*",
    "/",
    "%",
    "<=",
    "<",
    ">=",
    ">",
    "==",
    "|",
    "=",
    "+",
    "-",
    "[",
    "]",
    "{",
    "}",
    "(",
    ")",
]

keywords: list[str] = [
    "and",
    "bool",
    "call",
    "else",
    "false",
    "func",
    "if",
    "int",
    "length",
    "not",
    "or",
    "print",
    "return",
    "true",
    "var",
    "void",
    "while",
]

kinds: list[str] = ["ID", "INT", "EOF"] + punctuation + keywords
