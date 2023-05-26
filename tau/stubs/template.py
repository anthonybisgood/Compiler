# Description: Template for writing a visitor for the ASTs
# Copy and use as necessary
#
# The "ctx" parameter is used to pass information down the AST walk.
# It is not used in this template, but some compiler passes will use it.

from typing import Any

from tau import asts

# process is the entry point for the visitor
# It may need to be renamed to match the name of the pass
def process(ast: asts.Program):
    program(ast, None)


def id(ast: asts.Id, ctx: Any):
    pass


def idexpr(ast: asts.IdExpr, ctx: Any):
    id(ast.id, ctx)


def callexpr(ast: asts.CallExpr, ctx: Any):
    expr(ast.fn, ctx)
    for arg in ast.args:
        expr(arg, ctx)


def arraycell(ast: asts.ArrayCell, ctx: Any):
    expr(ast.arr, ctx)
    expr(ast.idx, ctx)


def intliteral(ast: asts.IntLiteral, ctx: Any):
    pass


def boolliteral(ast: asts.BoolLiteral, ctx: Any):
    pass


def binaryop(ast: asts.BinaryOp, ctx: Any):
    expr(ast.left, ctx)
    expr(ast.right, ctx)


def unaryop(ast: asts.UnaryOp, ctx: Any):
    expr(ast.expr, ctx)


def expr(ast: asts.Expr, ctx: Any):
    match ast:
        case asts.IdExpr():
            idexpr(ast, ctx)
        case asts.CallExpr():
            callexpr(ast, ctx)
        case asts.ArrayCell():
            arraycell(ast, ctx)
        case asts.IntLiteral():
            intliteral(ast, ctx)
        case asts.BoolLiteral():
            boolliteral(ast, ctx)
        case asts.BinaryOp():
            binaryop(ast, ctx)
        case asts.UnaryOp():
            unaryop(ast, ctx)
        case _:
            raise NotImplementedError(
                f"expr() not implemented for {type(ast)}"
            )


def inttype(ast: asts.IntType, ctx: Any):
    pass


def booltype(ast: asts.BoolType, ctx: Any):
    pass


def arraytype(ast: asts.ArrayType, ctx: Any):
    if ast.size is not None:
        expr(ast.size, ctx)
    typ(ast.element_type_ast, ctx)


def voidtype(ast: asts.VoidType, ctx: Any):
    pass


def typ(ast: asts.TypeAST, ctx: Any):
    match ast:
        case asts.IntType():
            inttype(ast, ctx)
        case asts.BoolType():
            booltype(ast, ctx)
        case asts.ArrayType():
            arraytype(ast, ctx)
        case asts.VoidType():
            voidtype(ast, ctx)
        case _:
            raise NotImplementedError(f"typ() not implemented for {type(ast)}")


def paramdecl(ast: asts.ParamDecl, ctx: Any):
    id(ast.id, ctx)
    typ(ast.type_ast, ctx)


def vardecl(ast: asts.VarDecl, ctx: Any):
    id(ast.id, ctx)
    typ(ast.type_ast, ctx)


def compoundstmt(ast: asts.CompoundStmt, ctx: Any):
    for decl in ast.decls:
        vardecl(decl, ctx)
    for s in ast.stmts:
        stmt(s, ctx)


def assignstmt(ast: asts.AssignStmt, ctx: Any):
    expr(ast.lhs, ctx)
    expr(ast.rhs, ctx)


def ifstmt(ast: asts.IfStmt, ctx: Any):
    expr(ast.expr, ctx)
    stmt(ast.thenStmt, ctx)
    if ast.elseStmt is not None:
        stmt(ast.elseStmt, ctx)


def whilestmt(ast: asts.WhileStmt, ctx: Any):
    expr(ast.expr, ctx)
    stmt(ast.stmt, ctx)


def returnstmt(ast: asts.ReturnStmt, ctx: Any):
    if ast.expr is not None:
        expr(ast.expr, ctx)


def callstmt(ast: asts.CallStmt, ctx: Any):
    callexpr(ast.call, ctx)


def printstmt(ast: asts.PrintStmt, ctx: Any):
    expr(ast.expr, ctx)


def stmt(ast: asts.Stmt, ctx: Any):
    match ast:
        case asts.CompoundStmt():
            compoundstmt(ast, ctx)
        case asts.AssignStmt():
            assignstmt(ast, ctx)
        case asts.IfStmt():
            ifstmt(ast, ctx)
        case asts.WhileStmt():
            whilestmt(ast, ctx)
        case asts.ReturnStmt():
            returnstmt(ast, ctx)
        case asts.CallStmt():
            callstmt(ast, ctx)
        case asts.PrintStmt():
            printstmt(ast, ctx)
        case _:
            raise NotImplementedError(
                f"stmt() not implemented for {type(ast)}"
            )


def funcdecl(ast: asts.FuncDecl, ctx: Any):
    id(ast.id, ctx)
    for param in ast.params:
        paramdecl(param, ctx)
    typ(ast.ret_type_ast, ctx)
    compoundstmt(ast.body, ctx)


def program(ast: asts.Program, ctx: Any):
    for decl in ast.decls:
        funcdecl(decl, ctx)
