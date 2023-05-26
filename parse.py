import typing
from tau import asts as ast, tokens
from tau import error


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner

    def getSpan(self, startToken: ast.AST, endToken: ast.AST) -> ast.Span:
        start: tokens.Coord = startToken.span.start
        end: tokens.Coord = endToken.span.end
        return ast.Span(start, end)

    def createArrayCell(
        self, name: ast.IdExpr, list: list[ast.Expr], endTokens: list[ast.Token]
    ) -> ast.ArrayCell:
        span: ast.Span = ast.Span(name.span.start, endTokens[0].span.end)
        res: ast.ArrayCell = ast.ArrayCell(name, list[0], span)
        for i in range(1, len(list)):
            span = ast.Span(
                name.span.start,
                endTokens[i].span.end,
            )
            res = ast.ArrayCell(res, list[i], span)
        return res

    def error(self, msg: str):
        error.error(msg, self.scanner.peek().span)

    def match(self, kind: str) -> tokens.Token:
        if self.current() != kind:
            self.error(f"expected {kind}")
        return self.scanner.consume()

    def current(self):
        return self.scanner.peek().kind

    def parse(self) -> ast.Program:
        v = self._grammar()
        self.match("EOF")
        return v

    # grammar -> funcDec { funcDec }
    def _grammar(self) -> ast.Program:
        decls: list["ast.FuncDecl"] = []
        decls.append(self._funcDec())
        while self.current() in {"func"}:
            decls.append(self._funcDec())
        span = self.getSpan(decls[0], decls[-1])
        _grammar_ = ast.Program(decls, span)
        return _grammar_

    # funcDec -> "func" ID "(" [ varNameType { "," varNameType } ] ")" [ ":" typeName ] compoundStmt
    def _funcDec(self) -> ast.FuncDecl:
        begin: ast.Token = self.match("func")
        funcId: ast.Id = ast.Id(self.match("ID"))
        self.match("(")
        params: list[ast.ParamDecl] = []
        if self.current() in {"ID"}:
            id_Type: tuple[ast.Id, ast.TypeAST] = self._varNameType()
            paramId: ast.Id = id_Type[0]
            paramType: ast.TypeAST = id_Type[1]
            paramDecl: ast.ParamDecl = ast.ParamDecl(
                paramId, paramType, self.getSpan(paramId, paramType)
            )
            params.append(paramDecl)
            while self.current() in {","}:
                self.match(",")
                id_Type: tuple[ast.Id, ast.TypeAST] = self._varNameType()
                paramId: ast.Id = id_Type[0]
                paramType: ast.TypeAST = id_Type[1]
                paramDecl: ast.ParamDecl = ast.ParamDecl(
                    paramId, paramType, self.getSpan(paramId, paramType)
                )
                params.append(paramDecl)
        self.match(")")
        # set it to void if no return type is specified
        retType: ast.TypeAST = ast.TypeAST()
        if self.current() in {":"}:
            self.match(":")
            retType = self._typeName()
        body: ast.CompoundStmt = self._compoundStmt()
        span = ast.Span(begin.span.start, body.span.end)
        _funcDec_ = ast.FuncDecl(funcId, params, retType, body, span)
        return _funcDec_

    # funcCall -> "call" ID funcAssignCall
    def _funcCall(self) -> ast.CallStmt:
        begin: ast.Token = self.match("call")
        id: ast.Id = ast.Id(self.match("ID"))
        idExpr: ast.IdExpr = ast.IdExpr(id, id.span)
        res: tuple[list[ast.Expr], ast.Token] = self._funcAssignCall()
        args: list[ast.Expr] = res[0]
        end: ast.Token = res[1]
        callStmtSpan: ast.Span = ast.Span(begin.span.start, end.span.end)
        callExprSpan: ast.Span = ast.Span(idExpr.span.start, end.span.end)
        callExpr: ast.CallExpr = ast.CallExpr(idExpr, args, callExprSpan)
        _funcCall_: ast.CallStmt = ast.CallStmt(callExpr, callStmtSpan)
        return _funcCall_

    # funcAssignCall -> "(" [ (expr) { "," (expr) } ] ")"
    def _funcAssignCall(self) -> tuple[list[ast.Expr], ast.Token]:
        self.match("(")
        args: list[ast.Expr] = []
        if self.current() in {"(", "-", "false", "not", "true", "ID", "INT"}:
            args.append(self._expr())
            while self.current() in {","}:
                self.match(",")
                args.append(self._expr())
        end: ast.Token = self.match(")")
        _funcAssignCall_ = args
        return _funcAssignCall_, end

    # compoundStmt -> "{" { varDec } { stmt } [ returnStmt ] "}"
    def _compoundStmt(self) -> ast.CompoundStmt:
        beginToken: ast.Token = self.match("{")
        varList: list[ast.VarDecl] = []
        stmtList: list[ast.Stmt] = []
        while self.current() in {"var"}:
            varList.append(self._varDec())
        while self.current() in {"call", "if", "print", "while", "{", "ID"}:
            stmtList.append(self._stmt())
        if self.current() in {"return"}:
            stmtList.append(self._returnStmt())
        endToken = self.match("}")
        span = ast.Span(beginToken.span.start, endToken.span.end)
        _compoundStmt_ = ast.CompoundStmt(varList, stmtList, span)
        return _compoundStmt_

    # stmt -> whileStmt | compoundStmt | ifStmt | print | funcCall | varAssignment
    def _stmt(self) -> ast.Stmt:
        if self.current() in {"while"}:
            _stmt_ = self._whileStmt()
        elif self.current() in {"{"}:
            _stmt_ = self._compoundStmt()
        elif self.current() in {"if"}:
            _stmt_ = self._ifStmt()
        elif self.current() in {"print"}:
            _stmt_ = self._print()
        elif self.current() in {"call"}:
            _stmt_ = self._funcCall()
        elif self.current() in {"ID"}:
            _stmt_ = self._varAssignment()
        else:
            self.error("syntax error")
            assert False
        return _stmt_

    # returnStmt -> "return" (expr)
    def _returnStmt(self) -> ast.ReturnStmt:
        begin: ast.Token = self.match("return")
        expresion: ast.Expr = self._expr()
        span = ast.Span(begin.span.start, expresion.span.end)
        _returnStmt_ = ast.ReturnStmt(expresion, span)
        return _returnStmt_

    # whileStmt -> "while" expr compoundStmt
    def _whileStmt(self) -> ast.WhileStmt:
        begin: ast.Token = self.match("while")
        expresson: ast.Expr = self._expr()
        compoundStmt: ast.CompoundStmt = self._compoundStmt()
        span: ast.Span = ast.Span(begin.span.start, compoundStmt.span.end)
        _whileStmt_ = ast.WhileStmt(expresson, compoundStmt, span)
        return _whileStmt_

    # ifStmt -> "if" expr compoundStmt [ "else" compoundStmt ]
    def _ifStmt(self) -> ast.IfStmt:
        begin: ast.Token = self.match("if")
        expresson: ast.Expr = self._expr()
        compoundStmt: ast.CompoundStmt = self._compoundStmt()
        elseStmt: ast.Optional[ast.CompoundStmt] = None
        if self.current() in {"else"}:
            self.match("else")
            elseStmt = self._compoundStmt()
        endCoord: tokens.Coord = (
            elseStmt.span.end if elseStmt else compoundStmt.span.end
        )
        span: ast.Span = ast.Span(begin.span.start, endCoord)
        _ifStmt_ = ast.IfStmt(expresson, compoundStmt, elseStmt, span)
        return _ifStmt_

    # print -> "print" (expr)
    def _print(self) -> ast.PrintStmt:
        begin = self.match("print")
        expression: ast.Expr = self._expr()
        span = ast.Span(begin.span.start, expression.span.end)
        _print_ = ast.PrintStmt(expression, span)
        return _print_

    # varAssignment -> ID [ arrayIndex ] "=" (expr)
    def _varAssignment(self) -> ast.AssignStmt:
        id: ast.Id = ast.Id(self.match("ID"))
        lhs: ast.IdExpr | ast.ArrayCell = ast.IdExpr(id, id.span)
        if self.current() in {"["}:
            res: tuple[list[ast.Expr], list[ast.Token]] = self._arrayIndex()
            arrayCells: list[ast.Expr] = res[0]
            endTokens: list[ast.Token] = res[1]
            lhs: ast.ArrayCell | ast.IdExpr = self.createArrayCell(
                lhs, arrayCells, endTokens
            )
        self.match("=")
        rhs: ast.Expr = self._expr()
        _varAssignment_ = ast.AssignStmt(
            lhs, rhs, ast.Span(lhs.span.start, rhs.span.end)
        )
        return _varAssignment_

    # expr -> expr1 { "or" expr1 }
    def _expr(self) -> ast.Expr:
        _expr_: ast.Expr = self._expr1()
        while self.current() in {"or"}:
            op: ast.Token = self.match("or")
            right: ast.Expr = self._expr1()
            span = self.getSpan(_expr_, right)
            _expr_ = ast.BinaryOp(op, _expr_, right, span)
        return _expr_

    # expr1 -> expr2 { "and" expr2 }
    def _expr1(self) -> ast.Expr:
        _expr_: ast.Expr = self._expr2()
        while self.current() in {"and"}:
            op: ast.Token = self.match("and")
            right: ast.Expr = self._expr2()
            _expr_ = ast.BinaryOp(op, _expr_, right, self.getSpan(_expr_, right))
        return _expr_

    # expr2 -> expr3 { operators expr3 }
    def _expr2(self) -> ast.Expr:
        _expr_2: ast.Expr = self._expr3()
        while self.current() in {"!=", "<", "<=", "==", ">", ">="}:
            op: ast.Token = self._operators()
            right: ast.Expr = self._expr3()
            _expr_2 = ast.BinaryOp(op, _expr_2, right, self.getSpan(_expr_2, right))
        return _expr_2

    # expr3 -> expr4 { subPlus expr4 }
    def _expr3(self) -> ast.Expr:
        _expr_3: ast.Expr = self._expr4()
        while self.current() in {"+", "-"}:
            op: ast.Token = self._subPlus()
            right: ast.Expr = self._expr4()
            _expr_3 = ast.BinaryOp(op, _expr_3, right, self.getSpan(_expr_3, right))
        return _expr_3

    # expr4 -> base { DivTimes base }
    def _expr4(self) -> ast.Expr:
        _expr_4: ast.Expr = self._base()
        while self.current() in {"*", "/"}:
            op: ast.Token = self._DivTimes()
            right: ast.Expr = self._base()
            _expr_4 = ast.BinaryOp(op, _expr_4, right, self.getSpan(_expr_4, right))
        return _expr_4

    # base -> [ "not" | "-" ] (ID [ funcAssignCall | arrayIndex ] | INT | bool | "(" expr ")")
    def _base(self) -> ast.Expr:
        unaryOpList: list[ast.Token] = []
        while self.current() in {"-", "not"}:
            if self.current() in {"not"}:
                unaryOpList.append(self.match("not"))
            elif self.current() in {"-"}:
                unaryOpList.append(self.match("-"))
            else:
                self.error("syntax error")
                assert False
        if self.current() in {"ID"}:
            id: ast.Id = ast.Id(self.match("ID"))
            spanStart: tokens.Coord = id.span.start
            idExpr: ast.IdExpr = ast.IdExpr(id, self.getSpan(id, id))
            _base_ = idExpr
            if self.current() in {"(", "["}:
                if self.current() in {"("}:
                    res1: tuple[list[ast.Expr], ast.Token] = self._funcAssignCall()
                    args: list[ast.Expr] = res1[0]
                    end = res1[1]
                    _base_ = ast.CallExpr(
                        idExpr,
                        args,
                        ast.Span(spanStart, end.span.end),
                    )
                elif self.current() in {"["}:
                    res: tuple[list[ast.Expr], list[ast.Token]] = self._arrayIndex()
                    _base_ = self.createArrayCell(idExpr, res[0], res[1])
                else:
                    self.error("syntax error")
                    assert False
        elif self.current() in {"INT"}:
            int: ast.Token = self.match("INT")
            span = ast.Span(int.span.start, int.span.end)
            _base_ = ast.IntLiteral(int, span)
        elif self.current() in {"false", "true"}:
            boolean: ast.Token = self._bool()
            value: bool = boolean.value == "true"
            span = ast.Span(boolean.span.start, boolean.span.end)
            _base_ = ast.BoolLiteral(boolean, value, span)
        elif self.current() in {"("}:
            self.match("(")
            _base_ = self._expr()
            self.match(")")
        else:
            self.error("syntax error")
            assert False
        for i in range(len(unaryOpList) - 1, -1, -1):
            op: ast.Token = unaryOpList[i]
            if i == 0 or i == len(unaryOpList) - 1:
                _base_ = ast.UnaryOp(
                    op, _base_, ast.Span(op.span.start, _base_.span.end)
                )
            else:
                _base_ = ast.UnaryOp(op, _base_, ast.Span(op.span.start, op.span.end))
        return _base_

    # varDec -> "var" varNameType
    def _varDec(self) -> ast.VarDecl:
        beginToken: ast.Token = self.match("var")
        id_Type: typing.Tuple[ast.Id, ast.TypeAST] = self._varNameType()
        id: ast.Id = id_Type[0]
        type: ast.TypeAST = id_Type[1]
        span: ast.Span = ast.Span(beginToken.span.start, type.span.end)
        _varDec_ = ast.VarDecl(id, type, span)
        return _varDec_

    # varNameType -> ID ":" typeName
    def _varNameType(self) -> typing.Tuple[ast.Id, ast.TypeAST]:
        astId: ast.Id = ast.Id(self.match("ID"))
        self.match(":")
        typeName: ast.TypeAST = self._typeName()
        return astId, typeName

    # arrayIndex -> "[" (expr) "]" { "[" (expr) "]" }
    def _arrayIndex(self) -> tuple[list[ast.Expr], list[ast.Token]]:
        self.match("[")
        topIndex: ast.Expr = self._expr()
        indicies: list[ast.Expr] = [topIndex]
        endTokens: list[ast.Token] = [(self.match("]"))]
        while self.current() in {"["}:
            self.match("[")
            indicies.append(self._expr())
            endTokens.append(self.match("]"))
        return indicies, endTokens

    # bool -> "true" | "false"
    def _bool(self) -> ast.Token:
        if self.current() in {"true"}:
            _bool_ = self.match("true")
        elif self.current() in {"false"}:
            _bool_ = self.match("false")
        else:
            self.error("syntax error")
            assert False
        return _bool_

    # typeName -> "void" | "int" | "bool" | ("[" [ expr ] "]" typeName)
    def _typeName(self) -> ast.TypeAST:
        if self.current() in {"void"}:
            _typeName_ = self.match("void")
            _typeName = ast.VoidType(_typeName_)
            _typeName.span = _typeName_.span
        elif self.current() in {"int"}:
            _typeName_ = self.match("int")
            _typeName = ast.IntType(_typeName_)
            _typeName.span = _typeName_.span
        elif self.current() in {"bool"}:
            _typeName_ = self.match("bool")
            _typeName = ast.BoolType(_typeName_)
            _typeName.span = _typeName_.span
        elif self.current() in {"["}:
            beginToken: ast.Token = self.match("[")
            size: ast.Optional["ast.Expr"] = None
            if self.current() in {"(", "-", "false", "not", "true", "ID", "INT"}:
                size = self._expr()
            self.match("]")
            arrTypeName: ast.TypeAST = self._typeName()
            span = ast.Span(beginToken.span.start, arrTypeName.span.end)
            arrType: ast.ArrayType = ast.ArrayType(size, arrTypeName, span)
            _typeName = arrType
        else:
            self.error("syntax error")
            assert False
        return _typeName

    # DivTimes -> "/" | "*"
    def _DivTimes(self) -> ast.Token:
        if self.current() in {"/"}:
            _DivTimes_ = self.match("/")
        elif self.current() in {"*"}:
            _DivTimes_ = self.match("*")
        else:
            self.error("syntax error")
            assert False
        return _DivTimes_

    # subPlus -> "-" | "+"
    def _subPlus(self) -> ast.Token:
        if self.current() in {"-"}:
            _subPlus_ = self.match("-")
        elif self.current() in {"+"}:
            _subPlus_ = self.match("+")
        else:
            self.error("syntax error")
            assert False
        return _subPlus_

    # operators -> "<" | "<=" | "==" | "!=" | ">" | ">="
    def _operators(self) -> ast.Token:
        if self.current() in {"<"}:
            _operators_ = self.match("<")
        elif self.current() in {"<="}:
            _operators_ = self.match("<=")
        elif self.current() in {"=="}:
            _operators_ = self.match("==")
        elif self.current() in {"!="}:
            _operators_ = self.match("!=")
        elif self.current() in {">"}:
            _operators_ = self.match(">")
        elif self.current() in {">="}:
            _operators_ = self.match(">=")
        else:
            self.error("syntax error")
            assert False
        return _operators_
