from typing import List

from tau import asts, symbols
from tau.vm.vm import (
    Equal,
    Insn,
    NotEqual,
    RestoreEvalStack,
    SaveEvalStack,
    Store,
    Print,
    Label,
    Jump,
    Add,
    Mul,
    Sub,
    Div,
    LessThan,
    LessThanEqual,
    GreaterThan,
    GreaterThanEqual,
    JumpIfNotZero,
    JumpIfZero,
    Load,
    PushFP,
    PushImmediate,
    PushSP,
    PushLabel,
    Negate,
    Not,
    Pop,
    PopFP,
    PopSP,
    JumpIndirect,
    Call,
    Halt,
    Noop,
    Swap,
)


# This is the entry point for the visitor.
def generate(ast: asts.Program) -> List[Insn]:
    return _Program(ast)


def _Program(ast: asts.Program) -> List[Insn]:
    for decl in ast.decls:
        f: List[Insn] = _FuncDecl(decl)


def _Stmt(ast: asts.Stmt) -> List[Insn]:
    if isinstance(ast, asts.AssignStmt):
        return _AssignStmt(ast)
    elif isinstance(ast, asts.IfStmt):
        return _IfStmt(ast)
    elif isinstance(ast, asts.WhileStmt):
        return _WhileStmt(ast)
    elif isinstance(ast, asts.CallStmt):
        return _CallStmt(ast)
    elif isinstance(ast, asts.CompoundStmt):
        return _CompoundStmt(ast)
    elif isinstance(ast, asts.PrintStmt):
        return _PrintStmt(ast)
    elif isinstance(ast, asts.ReturnStmt):
        return _ReturnStmt(ast)
    else:
        assert False, f"_Stmt() not implemented for {type(ast)}"


def rval_CallExpr(ast: asts.CallExpr) -> List[Insn]:
    # do pre-call stuff
    # do something with ast.fn
    for i, arg in enumerate(ast.args):
        # do something with arg
        pass
    # do post-call stuff


def _AssignStmt(ast: asts.AssignStmt) -> List[Insn]:
    # do something with ast.lhs
    # do something with ast.rhs
    pass


def _PrintStmt(ast: asts.PrintStmt) -> List[Insn]:
    # do something with ast.expr
    pass


def _IfStmt(ast: asts.IfStmt) -> List[Insn]:
    # do something with ast.expr
    # do something with ast.thenStmt
    # do something with ast.elseStmt
    pass


def _WhileStmt(ast: asts.WhileStmt) -> List[Insn]:
    # do something with ast.expr
    # do something with ast.stmt
    pass


# Generate the code such that control is transferred to the label
# if the expression evaluated to the "sense" value.
def control(e: asts.Expr, label: str, sense: bool) -> List[Insn]:
    match e:
        case asts.BinaryOp():
            return control_BinaryOp(e, label, sense)
        case asts.UnaryOp():
            return control_UnaryOp(e, label, sense)
        case asts.BoolLiteral():
            return control_BoolLiteral(e, label, sense)
        case _:
            # TODO: handle other cases
            pass


def control_BoolLiteral(
    e: asts.BoolLiteral, label: str, sense: bool
) -> List[Insn]:
    # TODO: implement
    pass


def control_BinaryOp(e: asts.BinaryOp, label: str, sense: bool) -> List[Insn]:
    match e.op.kind:
        case "and":
            # TODO: implement
            pass
        case "or":
            # TODO: implement
            pass
        case _:
            # TODO: handle other cases
            pass


def control_UnaryOp(e: asts.UnaryOp, label: str, sense: bool) -> List[Insn]:
    match e.op.kind:
        case "not":
            # TODO: implement
            pass
        case _:
            assert False, f"control_UnaryOp() not implemented for {e.op.kind}"


def _CallStmt(ast: asts.CallStmt) -> List[Insn]:
    # do something with ast.call
    pass


def _CompoundStmt(ast: asts.CompoundStmt) -> List[Insn]:
    for stmt in ast.stmts:
        v = _Stmt(stmt)


def _FuncDecl(ast: asts.FuncDecl) -> List[Insn]:
    # do something for prologue
    c: List[Insn] = _CompoundStmt(ast.body)
    # do something for epilogue


def _ReturnStmt(ast: asts.ReturnStmt) -> List[Insn]:
    # do something with ast.expr, if present
    pass


def lval(e: asts.Expr) -> List[Insn]:
    match e:
        case asts.IdExpr():
            return lval_IdExpr(e)
        case _:
            assert False, f"lval() not implemented for {type(e)}"


def lval_IdExpr(e: asts.IdExpr) -> List[Insn]:
    assert isinstance(e.id.symbol, symbols.IdSymbol)
    match type(e.id.symbol.scope):
        case symbols.GlobalScope:
            # TODO: implement
            pass
        case symbols.LocalScope:
            # TODO: implement
            pass
        case symbols.FuncScope:
            # TODO: implement
            pass
        case _:
            assert (
                False
            ), f"lval_id() not implemented for {type(e.id.symbol.scope)}"


def rval(e: asts.Expr) -> List[Insn]:
    match e:
        case asts.BinaryOp():
            return rval_BinaryOp(e)
        case asts.UnaryOp():
            return rval_UnaryOp(e)
        case asts.CallExpr():
            return rval_CallExpr(e)
        case asts.IdExpr():
            return rval_IdExpr(e)
        case asts.IntLiteral():
            return rval_IntLiteral(e)
        case asts.BoolLiteral():
            return rval_BoolLiteral(e)
        case _:
            assert False, f"rval() not implemented for {type(e)}"


def rval_BoolLiteral(e: asts.BoolLiteral) -> List[Insn]:
    # TODO: implement
    pass


def rval_IntLiteral(e: asts.IntLiteral) -> List[Insn]:
    # TODO: implement
    pass


def rval_IdExpr(e: asts.IdExpr) -> List[Insn]:
    # TODO: implement
    pass


def rval_BinaryOp(e: asts.BinaryOp) -> List[Insn]:
    match e.op.kind:
        case "+":
            # TODO: implement
            pass
        case "-":
            # TODO: implement
            pass
        case "*":
            # TODO: implement
            pass
        case "/":
            # TODO: implement
            pass
        case "<":
            # TODO: implement
            pass
        case "<=":
            # TODO: implement
            pass
        case ">":
            # TODO: implement
            pass
        case ">=":
            # TODO: implement
            pass
        case "==":
            # TODO: implement
            pass
        case "!=":
            # TODO: implement
            pass
        case "and":
            # TODO: implement
            pass
        case "or":
            # TODO: implement
            pass
        case _:
            assert False, f"rval_BinaryOp() not implemented for {e.op}"


def rval_UnaryOp(e: asts.UnaryOp) -> List[Insn]:
    match e.op.kind:
        case "-":
            # TODO: implement
            pass
        case "not":
            # TODO: implement
            pass
        case _:
            assert False, f"rval_UnaryOp() not implemented for {e.op}"
