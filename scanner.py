from tau import tokens, error
from tau.tokens import Span, Coord, Token, punctuation, keywords
import string


class Scanner:
    def __init__(self, input: str):
        self.input = input
        self.tokenArray: list = []
        self.DELIMITERS: set = {" ", "(", ")"}
        row: int = 1
        column: int = 1
        i: int = 0
        tokenVal: str = ""
        while i < len(input):
            l = input[i]
            # If comment line interate i until out of comment line
            if input[i : i + 2] == '//':
                self.createToken(tokenVal, row, column)
                tokenVal = ""
                while i < len(input) and input[i] != "\n":
                    i += 1
                column = 1
                row += 1
            # if newline reset column and iterate row
            elif l == "\n":
                self.createToken(tokenVal, row, column)
                tokenVal = ""
                row += 1
                column = 1
            elif l == " ":
                self.createToken(tokenVal, row, column)
                tokenVal = ""
                column += 1
            elif l in punctuation or l == "!":
                self.createToken(tokenVal, row, column)
                column += 1
                if (
                    l in {"!", "<", ">", "="}
                    and i + 1 < len(input)
                    and input[i + 1] == "="
                ):
                    column += 1
                    self.createToken(l + "=", row, column)
                    i += 1
                    tokenVal = ""
                elif l != "!":
                    self.createToken(l, row, column)
                    tokenVal = ""
                else:
                    tokenVal += l
            elif l in string.ascii_letters:
                # if we find a letter after an integer
                if tokenVal and tokenVal[0].isdigit():
                    self.createToken(tokenVal, row, column)
                    tokenVal = ""
                tokenVal += l
                column += 1
            # if on a digit and token is already a digit or empty
            elif l in string.digits:
                if tokenVal == "" or tokenVal[0].isdigit():
                    tokenVal += l
                    column += 1
                elif tokenVal[0] in string.ascii_letters:
                    tokenVal += l
                    column += 1
            elif l == "\t":
                column += 1
            elif l not in punctuation or l not in keywords:
                Error_cord: Coord = Coord(column, row)
                Error_span: Span = Span(Error_cord, Error_cord)

                msg: str = str.format("Not in language: {0}", ascii(l))
                error.error(msg, Error_span)
            if tokenVal in keywords:
                # if the token thats already a keyword has more text at the end of it
                if (
                    i + 1 < len(input)
                    and input[i + 1] not in string.digits
                    and input[i + 1] not in string.ascii_letters
                ):
                    self.createToken(tokenVal, row, column)
                    tokenVal = ""
            i += 1
        EOF_cord: Coord = Coord(column, row)
        EOF_span: Span = Span(EOF_cord, EOF_cord)
        EOF_token: Token = Token("EOF", "", EOF_span)
        self.tokenArray.append(EOF_token)

    def createToken(self, tokenVal, row, col):
        if not tokenVal:
            return
        if tokenVal in keywords or tokenVal in punctuation:
            tokenKind = tokenVal
        else:
            tokenKind = "ID" if tokenVal[0] in string.ascii_letters else "INT"
        token_start: Coord = Coord(col - len(tokenVal), row)
        token_end: Coord = Coord(col, row)
        token_span: Span = Span(token_start, token_end)
        token: Token = Token(tokenKind, tokenVal, token_span)
        self.tokenArray.append(token)

    def peek(self) -> Token:
        return self.tokenArray[0]

    def consume(self) -> Token:
        return self.tokenArray.pop(0)
