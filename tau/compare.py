from typing import Callable
from .asts import (
    AST,
    Program,
    FuncDecl,
    Id,
    VarDecl,
    ParamDecl,
    IntType,
    BoolType,
    VoidType,
    ArrayType,
    PrintStmt,
    CompoundStmt,
    CallExpr,
    AssignStmt,
    IfStmt,
    WhileStmt,
    ReturnStmt,
    CallStmt,
    BinaryOp,
    UnaryOp,
    ArrayCell,
    IdExpr,
    IntLiteral,
    BoolLiteral,
)


def assert_equal(
    correct: AST, other: AST, fn: Callable[[AST, AST], bool]
) -> bool:
    match correct:
        case Program():
            assert isinstance(
                other, Program
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert len(correct.decls) == len(
                other.decls
            ), f"{len(correct.decls)} != {len(other.decls)}"
            for i in range(len(correct.decls)):
                assert_equal(correct.decls[i], other.decls[i], fn)
            fn(correct, other)
        case Id():
            assert isinstance(other, Id), f"{type(correct)} != {type(other)}"
            assert (
                correct.token == other.token
            ), f"{correct.token} != {other.token}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            fn(correct, other)
        case VarDecl():
            assert isinstance(
                other, VarDecl
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.id, other.id, fn)
            assert_equal(correct.type_ast, other.type_ast, fn)
            fn(correct, other)
        case ParamDecl():
            assert isinstance(
                other, ParamDecl
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.id, other.id, fn)
            assert_equal(correct.type_ast, other.type_ast, fn)
            fn(correct, other)
        case IntType():
            assert isinstance(
                other, IntType
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.token == other.token
            ), f"{correct.token} != {other.token}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            fn(correct, other)
        case BoolType():
            assert isinstance(
                other, BoolType
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.token == other.token
            ), f"{correct.token} != {other.token}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            fn(correct, other)
        case VoidType():
            assert isinstance(
                other, VoidType
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.token == other.token
            ), f"{correct.token} != {other.token}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            fn(correct, other)
        case ArrayType():
            assert isinstance(
                other, ArrayType
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert (correct.size == None and other.size == None) or (
                correct.size != None
                and other.size != None
                and assert_equal(correct.size, other.size, fn)
            )
            assert_equal(correct.element_type_ast, other.element_type_ast, fn)
            fn(correct, other)
        case PrintStmt():
            assert isinstance(
                other, PrintStmt
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.expr, other.expr, fn)
            fn(correct, other)
        case CompoundStmt():
            assert isinstance(
                other, CompoundStmt
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert len(correct.decls) == len(
                other.decls
            ), f"{len(correct.decls)} != {len(other.decls)}"
            for i in range(len(correct.decls)):
                assert_equal(correct.decls[i], other.decls[i], fn)
            assert len(correct.stmts) == len(
                other.stmts
            ), f"{len(correct.stmts)} != {len(other.stmts)}"
            for i in range(len(correct.stmts)):
                assert_equal(correct.stmts[i], other.stmts[i], fn)
            fn(correct, other)
        case CallStmt():
            assert isinstance(
                other, CallStmt
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.call, other.call, fn)
            fn(correct, other)
        case FuncDecl():
            assert isinstance(
                other, FuncDecl
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.id, other.id, fn)
            assert len(correct.params) == len(
                other.params
            ), f"{len(correct.params)} != {len(other.params)}"
            for i in range(len(correct.params)):
                assert_equal(correct.params[i], other.params[i], fn)
            assert_equal(correct.ret_type_ast, other.ret_type_ast, fn)
            assert_equal(correct.body, other.body, fn)
            fn(correct, other)
        case CallExpr():
            assert isinstance(
                other, CallExpr
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.fn, other.fn, fn)
            assert len(correct.args) == len(
                other.args
            ), f"{len(correct.args)} != {len(other.args)}"
            for i in range(len(correct.args)):
                assert_equal(correct.args[i], other.args[i], fn)
            fn(correct, other)
        case AssignStmt():
            assert isinstance(
                other, AssignStmt
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.lhs, other.lhs, fn)
            assert_equal(correct.rhs, other.rhs, fn)
            fn(correct, other)
        case IfStmt():
            assert isinstance(
                other, IfStmt
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.expr, other.expr, fn)
            assert_equal(correct.thenStmt, other.thenStmt, fn)
            assert (correct.elseStmt == None and other.elseStmt == None) or (
                correct.elseStmt != None
                and other.elseStmt != None
                and assert_equal(correct.elseStmt, other.elseStmt, fn)
            )
            fn(correct, other)
        case WhileStmt():
            assert isinstance(
                other, WhileStmt
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.expr, other.expr, fn)
            assert_equal(correct.stmt, other.stmt, fn)
            fn(correct, other)
        case ReturnStmt():
            assert isinstance(
                other, ReturnStmt
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert (correct.expr == None and other.expr == None) or (
                correct.expr != None
                and other.expr != None
                and assert_equal(correct.expr, other.expr, fn)
            )
            fn(correct, other)
        case BinaryOp():
            assert isinstance(
                other, BinaryOp
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert correct.op == other.op, f"{correct.op} != {other.op}"
            assert_equal(correct.left, other.left, fn)
            assert_equal(correct.right, other.right, fn)
            fn(correct, other)
        case UnaryOp():
            assert isinstance(
                other, UnaryOp
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert correct.op == other.op, f"{correct.op} != {other.op}"
            assert_equal(correct.expr, other.expr, fn)
            fn(correct, other)
        case ArrayCell():
            assert isinstance(
                other, ArrayCell
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.arr, other.arr, fn)
            assert_equal(correct.idx, other.idx, fn)
            fn(correct, other)
        case IntLiteral():
            assert isinstance(
                other, IntLiteral
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert (
                correct.token == other.token
            ), f"{correct.token} != {other.token}"
            fn(correct, other)
        case BoolLiteral():
            assert isinstance(
                other, BoolLiteral
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert (
                correct.value == other.value
            ), f"{correct.value} != {other.value}"
            fn(correct, other)
        case IdExpr():
            assert isinstance(
                other, IdExpr
            ), f"{type(correct)} != {type(other)}"
            assert (
                correct.span == other.span
            ), f"{correct.span} != {other.span}"
            assert_equal(correct.id, other.id, fn)
            fn(correct, other)
        case _:  # pragma: no cover
            raise NotImplementedError(
                "Unknown AST node type: " + str(type(correct))
            )

    return True
