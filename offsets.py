from tau import asts, error

# process is the entry point for the visitor
# It may need to be renamed to match the name of the pass
def process(ast: asts.Program):
    program(ast)


def id(ast: asts.Id, offset: int):
    pass


def idexpr(ast: asts.IdExpr, offset: int):
    id(ast.id, offset)


def callexpr(ast: asts.CallExpr, offset: int):
    expr(ast.fn, offset)
    for arg in ast.args:
        expr(arg, offset)


def arraycell(ast: asts.ArrayCell, offset: int):
    expr(ast.arr, offset)
    expr(ast.idx, offset)


def intliteral(ast: asts.IntLiteral, offset: int):
    pass


def boolliteral(ast: asts.BoolLiteral, offset: int):
    pass


def binaryop(ast: asts.BinaryOp, offset: int):
    expr(ast.left, offset)
    expr(ast.right, offset)


def unaryop(ast: asts.UnaryOp, offset: int):
    expr(ast.expr, offset)


def expr(ast: asts.Expr, offset: int):
    match ast:
        case asts.IdExpr():
            idexpr(ast, offset)
        case asts.CallExpr():
            callexpr(ast, offset)
        case asts.ArrayCell():
            arraycell(ast, offset)
        case asts.IntLiteral():
            intliteral(ast, offset)
        case asts.BoolLiteral():
            boolliteral(ast, offset)
        case asts.BinaryOp():
            binaryop(ast, offset)
        case asts.UnaryOp():
            unaryop(ast, offset)
        case _:
            error.error(f"expr() not implemented for {type(ast)}", ast.span)


def inttype(ast: asts.IntType, offset: int):
    pass


def booltype(ast: asts.BoolType, offset: int):
    pass


def arraytype(ast: asts.ArrayType, offset: int):
    if ast.size is not None:
        expr(ast.size, offset)
    typ(ast.element_type_ast, offset)


def voidtype(ast: asts.VoidType, offset: int):
    pass


def typ(ast: asts.TypeAST, offset: int):
    match ast:
        case asts.IntType():
            inttype(ast, offset)
        case asts.BoolType():
            booltype(ast, offset)
        case asts.ArrayType():
            arraytype(ast, offset)
        case asts.VoidType():
            voidtype(ast, offset)
        case _:
            error.error(f"typ() not implemented for {type(ast)}", ast.span)


def paramdecl(ast: asts.ParamDecl, offset: int):
    id(ast.id, offset)
    ast.id.symbol.offset = offset
    typ(ast.type_ast, offset)


def vardecl(ast: asts.VarDecl, offset: int):
    id(ast.id, offset)
    ast.id.symbol.offset = offset
    typ(ast.type_ast, offset)


def compoundstmt(ast: asts.CompoundStmt, offset: int) -> int:
    max_offset = offset
    for decl in ast.decls:
        vardecl(decl, offset)
        offset += 1
    for s in ast.stmts:
        max_offset = max(stmt(s, offset), max_offset)
    max_offset = max(max_offset, offset)
    return max_offset


def assignstmt(ast: asts.AssignStmt, offset: int):
    expr(ast.lhs, offset)
    expr(ast.rhs, offset)


def ifstmt(ast: asts.IfStmt, offset: int):
    expr(ast.expr, offset)
    stmt(ast.thenStmt, offset)
    if ast.elseStmt is not None:
        stmt(ast.elseStmt, offset)


def whilestmt(ast: asts.WhileStmt, offset: int):
    expr(ast.expr, offset)
    stmt(ast.stmt, offset)


def returnstmt(ast: asts.ReturnStmt, offset: int):
    if ast.expr is not None:
        expr(ast.expr, offset)


def callstmt(ast: asts.CallStmt, offset: int):
    callexpr(ast.call, offset)

def printstmt(ast: asts.PrintStmt, offset: int):
    expr(ast.expr, offset)


def stmt(ast: asts.Stmt, offset: int) -> int:
    paramSize: int = 0
    match ast:
        case asts.CompoundStmt():
            paramSize = compoundstmt(ast, offset)
        case asts.AssignStmt():
            assignstmt(ast, offset)
        case asts.IfStmt():
            ifstmt(ast, offset)
        case asts.WhileStmt():
            whilestmt(ast, offset)
        case asts.ReturnStmt():
            returnstmt(ast, offset)
        case asts.CallStmt():
            callstmt(ast, offset)
            paramSize += len(ast.call.args)
        case asts.PrintStmt():
            printstmt(ast, offset)
        case _:
            error.error(f"stmt() not implemented for {type(ast)}", ast.span)
    return paramSize

def funcdecl(ast: asts.FuncDecl):
    offset: int = 0
    id(ast.id, offset)
    numParams: int = 0
    for param in ast.params:
        ParamOffset: int = -2 - numParams
        paramdecl(param, ParamOffset)
        numParams += 1
    typ(ast.ret_type_ast, offset)
    offset: int = 3
    max_offset = compoundstmt(ast.body, offset)
    ast.size = max_offset + 4# +1 for return address +3 for bookkeeping


def program(ast: asts.Program):
    for decl in ast.decls:
        funcdecl(decl)
