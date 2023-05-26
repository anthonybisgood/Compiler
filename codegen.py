from typing import List

from tau import asts, symbols, error
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
    res: List[Insn] = []
    res.append(PushLabel("main"))
    res.append(Call())
    res.append(Halt())
    for decl in ast.decls:
        res.append(Label(decl.id.token.value))
        f: List[Insn] = _FuncDecl(decl)
        res.extend(f)
    res.append(Halt())
    return res


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
    res: List[Insn] = []
    # do pre-call stuff
    for i, arg in enumerate(ast.args):
        res.append(PushSP(-i - 2))
        res.extend(rval(arg))
        res.append(Store())
    # do something with ast.fn
    res.extend(lval(ast.fn))
    res.append(Call())
    # do post-call stuff
    res.append(PushSP(-1))
    res.append(Load())
    return res


def _AssignStmt(ast: asts.AssignStmt) -> List[Insn]:
    res: List[Insn] = []
    res.extend(lval(ast.lhs))
    res.extend(rval(ast.rhs))
    res.append(Store())
    return res


def _PrintStmt(ast: asts.PrintStmt) -> List[Insn]:
    res: List[Insn] = []
    res.extend(rval(ast.expr))
    res.append(Print())
    return res


def _IfStmt(ast: asts.IfStmt) -> List[Insn]:
    res: List[Insn] = []
    elselabel: str = "else" + str(id(ast))
    exitlabel: str = "exit" + str(id(ast))
    elseLabel: Label = Label(elselabel)
    exitLabel: Label = Label(exitlabel)
    ############################################################
    res.extend(control(ast.expr, elselabel, False))
    res.extend(_Stmt(ast.thenStmt))
    res.append(Jump(exitlabel))
    # add elseLabel here
    res.append(elseLabel)
    if ast.elseStmt:
        res.extend(_Stmt(ast.elseStmt))
    res.append(exitLabel)
    return res


def _WhileStmt(ast: asts.WhileStmt) -> List[Insn]:
    res: List[Insn] = []
    toplabel: str = "top" + str(id(ast))
    exitlabel: str = "exit" + str(id(ast))
    topLabel: Label = Label(toplabel)
    exitLabel: Label = Label(exitlabel)
    ############################################################
    res.append(topLabel)
    res.extend(control(ast.expr, exitlabel, False))
    res.extend(_Stmt(ast.stmt))
    res.append(Jump(toplabel))
    res.append(exitLabel)
    return res


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
        case asts.IdExpr():
            return control_IdExpr(e, label, sense)
        case asts.CallExpr():
            return control_CallExpr(e, label, sense)
        case _:
            error.error(f"control() not implemented for {type(e)}", e.span)   

def control_CallExpr(e: asts.CallExpr, label: str, sense: bool) -> List[Insn]:
    res: List[Insn] = []
    res.extend(rval(e))
    if sense:
        res.append(JumpIfNotZero(label))
    else:
        res.append(JumpIfZero(label))
    return res


def control_IdExpr(e: asts.IdExpr, label: str, sense: bool) -> List[Insn]:
    res: List[Insn] = []
    res.extend(rval(e))
    if sense:
        res.append(JumpIfNotZero(label))
    else:
        res.append(JumpIfZero(label))
    return res


def control_BoolLiteral(e: asts.BoolLiteral, label: str, sense: bool) -> List[Insn]:
    res: List[Insn] = []
    if e.value == sense:
        res.append(Jump(label))
    return res


def control_BinaryOp(e: asts.BinaryOp, label: str, sense: bool) -> List[Insn]:
    res: List[Insn] = []
    exitlabel: str = "exit" + str(id(e))
    exitLabel: Label = Label(exitlabel)
    match e.op.kind:
        case "and":
            if sense:
                res.extend(control(e.left, exitlabel, False))
                res.extend(control(e.right, label, True))
                res.append(exitLabel)
            else:
                res.extend(control(e.left, label, False))
                res.extend(control(e.right, label, False))
        case "or":
            if sense:
                res.extend(control(e.left, label, True))
                res.extend(control(e.right, label, True))
            else:
                res.extend(control(e.left, exitlabel, True))
                res.extend(control(e.right, label, False))
                res.append(exitLabel)
        case "<" | "<=" | ">" | ">=" | "==" | "!=":
            insns: dict[str, Insn] = {
                "<": LessThan(),
                "<=": LessThanEqual(),
                ">": GreaterThan(),
                ">=": GreaterThanEqual(),
                "==": Equal(),
                "!=": NotEqual(),
            }
            res.extend(rval(e.left))
            res.extend(rval(e.right))
            res.append(insns[e.op.kind])
            if sense:
                res.append(JumpIfNotZero(label))
            else:
                res.append(JumpIfZero(label))
        case _:
            error.error(f"control_BinaryOp() not implemented for {e.op.kind}", e.op.span)
    return res


def control_UnaryOp(e: asts.UnaryOp, label: str, sense: bool) -> List[Insn]:
    match e.op.kind:
        case "not":
            return control(e.expr, label, not sense)
        case _:
            assert False, f"control_UnaryOp() not implemented for {e.op.kind}"


def _CallStmt(ast: asts.CallStmt) -> List[Insn]:
    res: List[Insn] = []
    res.extend(rval(ast.call))
    return res


def _CompoundStmt(ast: asts.CompoundStmt) -> List[Insn]:
    res: List[Insn] = []
    for stmt in ast.stmts:
        v = _Stmt(stmt)
        res.extend(v)
    return res


def _FuncDecl(ast: asts.FuncDecl) -> List[Insn]:
    res: List[Insn] = []
    # if ast.id.token.value == "f":
    #     raise Exception(ast.size)
    # do something for prologue
    prolog: List[Insn] = []
    offset: int = ast.size
    # # push callees return address at offset 0 from callee fp
    ############################################################
    prolog.append(PushSP(0, "address offset 0 from callers Sp"))
    prolog.append(Swap())
    prolog.append(Store())
    # push callees Fp at offset 1 from fp
    prolog.append(PushSP(1, "address offset 1 from callers Sp"))
    prolog.append(PushFP(0, "FP value to save"))
    prolog.append(Store())
    # push callers Sp at offset 2 from fp
    prolog.append(PushSP(2, "address offset 2 from callers Sp"))
    prolog.append(PushSP(0, "SP value to save"))
    prolog.append(Store())
    # set callee fp to caller stack pointer
    prolog.append(PushSP(0, "push current sp to stack"))
    prolog.append(PopFP("set fp to sp, pop sp from stack"))
    # set callee sp to caller sp + offset
    prolog.append(PushSP(offset, "push new sp + offfset to stack"))
    prolog.append(PopSP("set sp to new sp + offset"))
    res.extend(prolog)
    # compund stmt
    c: List[Insn] = _CompoundStmt(ast.body)
    res.extend(c)
    # do something for epilogue
    epilogue: List[Insn] = []
    # push the return address 
    epilogue.append(PushFP(0))
    epilogue.append(Load())
    # push the callers fp
    epilogue.append(PushFP(2, "push callers fp to stack"))
    epilogue.append(Load())
    epilogue.append(PopSP())
    # push the callers sp
    epilogue.append(PushFP(1, "push callers sp to stack"))
    epilogue.append(Load())
    epilogue.append(PopFP())
    # jump to return address
    epilogue.append(JumpIndirect())
    res.extend(epilogue)
    return res

def _ReturnStmt(ast: asts.ReturnStmt) -> List[Insn]:
    res: List[Insn] = []
    if ast.expr:
        res.append(PushFP(-1))
        res.extend(rval(ast.expr))
        res.append(Store())
    res.append(PushFP(0))
    res.append(Load())
    res.append(PushFP(2, "push callers fp to stack"))
    res.append(Load())
    res.append(PopSP())

    res.append(PushFP(1, "push callers sp to stack"))
    res.append(Load())
    res.append(PopFP())
    res.append(JumpIndirect())
    return res


def lval(e: asts.Expr) -> List[Insn]:
    match e:
        case asts.IdExpr():
            return lval_IdExpr(e)
        case _:
            assert False, f"lval() not implemented for {type(e)}"


def lval_IdExpr(e: asts.IdExpr) -> List[Insn]:
    assert isinstance(e.id.symbol, symbols.IdSymbol)
    res: List[Insn] = []
    offset: int = e.id.symbol.offset
    match type(e.id.symbol.scope):
        case symbols.GlobalScope:
            res.append(PushLabel(e.id.token.value))
        case symbols.LocalScope:
            res.append(PushFP(offset))
        case symbols.FuncScope:
            res.append(PushFP(offset))
        case _:
            assert False, f"lval_id() not implemented for {type(e.id.symbol.scope)}"
    return res


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
    res: List[Insn] = []
    if e.token.value == "true":
        res.append(PushImmediate(1))
    else:
        res.append(PushImmediate(0))
    return res


def rval_IntLiteral(e: asts.IntLiteral) -> List[Insn]:
    res: List[Insn] = []
    res.append(PushImmediate(int(e.token.value)))
    return res


def rval_IdExpr(e: asts.IdExpr) -> List[Insn]:
    res: List[Insn] = []
    res.extend(lval(e))
    res.append(Load())
    return res


def rval_BinaryOp(e: asts.BinaryOp) -> List[Insn]:
    res: List[Insn] = []
    if e.op.kind in ["+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!="]:
        res.extend(rval(e.left))
        res.extend(rval(e.right))
    match e.op.kind:
        case "+":
            res.append(Add())
        case "-":
            res.append(Sub())
        case "*":
            res.append(Mul())
        case "/":
            res.append(Div())
        case "<":
            res.append(LessThan())
        case "<=":
            res.append(LessThanEqual())
        case ">":
            res.append(GreaterThan())
        case ">=":
            res.append(GreaterThanEqual())
        case "==":
            res.append(Equal())
        case "!=":
            res.append(NotEqual())
        case "and" | "or" | "not":
            trueLabel: str = f"true_{id(e)}"
            exitLabel: str = f"exit_{id(e)}"
            res.extend(control(e, trueLabel, True))
            res.append(PushImmediate(0))
            res.append(Jump(exitLabel))
            res.append(Label(trueLabel))
            res.append(PushImmediate(1))
            res.append(Label(exitLabel))
        case _:
            assert False, f"rval_BinaryOp() not implemented for {e.op}"
    return res


def rval_UnaryOp(e: asts.UnaryOp) -> List[Insn]:
    res: List[Insn] = []
    match e.op.kind:
        case "-":
            res.extend(rval(e.expr))
            res.append(PushImmediate(-1))
            res.append(Mul())
        case "not":
            res.append(PushImmediate(1))
            res.extend(rval(e.expr))
            res.append(Sub())
        case _:
            assert False, f"rval_UnaryOp() not implemented for {e.op}"
    return res
