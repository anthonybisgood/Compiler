from typing import NoReturn

from .tokens import Span


class CompilerError(Exception):
    def __init__(self, msg: str, span: Span):
        self.msg = msg
        self.span = span

    def __str__(self):
        return f"{self.span.start}: {self.msg}"


def error(msg: str, span: Span) -> NoReturn:
    raise CompilerError(msg, span)
