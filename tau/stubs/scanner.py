from tau import tokens, error
from tau.tokens import Span, Coord, Token, punctuation, keywords


class Scanner:
    def __init__(self, input: str):
        pass  # edit this routine

    def peek(self) -> Token:
        pass  # edit this routine

    def consume(self) -> Token:
        pass  # edit this routine
