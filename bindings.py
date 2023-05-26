from tau import asts, symbols, error

def bind(ast: asts.Program):
    process(ast)
    return ast


# Path: project-anthonybisgood\main.py# Description: Template for writing a visitor for the ASTs
# Copy and use as necessary
#
# The "ctx" parameter is used to pass information down the AST walk.
# It is not used in this template, but some compiler passes will use it.

# process is the entry point for the visitor
# It may need to be renamed to match the name of the pass
def process(ast: asts.Program):
    program(ast)


def id(ast: asts.Id, ctx: symbols.Scope):
    name: str = ast.token.value
    table = ctx.symtab
    while name not in table and ctx.parent is not None:
        ctx = ctx.parent
        table = ctx.symtab
    if name not in table:
        error.error(f"Undefined identifier {name}", ast.span)
    ast.symbol = ctx.symtab[name]
        
def idexpr(ast: asts.IdExpr, ctx: symbols.Scope):
    id(ast.id, ctx)


def callexpr(ast: asts.CallExpr, ctx: symbols.Scope):
    expr(ast.fn, ctx)
    for arg in ast.args:
        expr(arg, ctx)


def arraycell(ast: asts.ArrayCell, ctx: symbols.Scope):
    expr(ast.arr, ctx)
    expr(ast.idx, ctx)


def intliteral(ast: asts.IntLiteral, ctx: symbols.Scope):
    pass


def boolliteral(ast: asts.BoolLiteral, ctx: symbols.Scope):
    pass


def binaryop(ast: asts.BinaryOp, ctx: symbols.Scope):
    expr(ast.left, ctx)
    expr(ast.right, ctx)


def unaryop(ast: asts.UnaryOp, ctx: symbols.Scope):
    expr(ast.expr, ctx)


def expr(ast: asts.Expr, ctx: symbols.Scope):
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
            error.error(f"expr() not implemented for {type(ast)}", ctx.span)


def inttype(ast: asts.IntType, ctx: symbols.Scope):
    pass


def booltype(ast: asts.BoolType, ctx: symbols.Scope):
    pass


def arraytype(ast: asts.ArrayType, ctx: symbols.Scope):
    if ast.size is not None:
        expr(ast.size, ctx)
    typ(ast.element_type_ast, ctx)


def voidtype(ast: asts.VoidType, ctx: symbols.Scope):
    pass


def typ(ast: asts.TypeAST, ctx: symbols.Scope):
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
            error.error(f"typ() not implemented for {type(ast)}", ctx.span)


def paramdecl(ast: asts.ParamDecl, ctx: symbols.Scope):
    id(ast.id, ctx)
    typ(ast.type_ast, ctx)
    
def vardecl(ast: asts.VarDecl, ctx: symbols.Scope):
    id(ast.id, ctx)
    typ(ast.type_ast, ctx)

def compoundstmt(ast: asts.CompoundStmt, ctx: symbols.Scope):
    scope = symbols.LocalScope(ctx, ast.span)
    symtab: dict = {}
    scope.symtab = symtab
    ast.local_scope = scope
    for decl in ast.decls:
        newIdSymbol = symbols.IdSymbol(decl.id.token.value, scope)
        name = decl.id.token.value
        symtab[name] = newIdSymbol
        vardecl(decl, scope)
    for s in ast.stmts:
        stmt(s, scope)


def assignstmt(ast: asts.AssignStmt, ctx: symbols.Scope):
    expr(ast.lhs, ctx)
    expr(ast.rhs, ctx)


def ifstmt(ast: asts.IfStmt, ctx: symbols.Scope):
    expr(ast.expr, ctx)
    stmt(ast.thenStmt, ctx)
    if ast.elseStmt is not None:
        stmt(ast.elseStmt, ctx)


def whilestmt(ast: asts.WhileStmt, ctx: symbols.Scope):
    expr(ast.expr, ctx)
    stmt(ast.stmt, ctx)


def returnstmt(ast: asts.ReturnStmt, ctx: symbols.Scope):
    if ast.enclosing_scope is None:
        error.error("Return statement outside of function", ast.span)
    if ast.expr is not None:
        expr(ast.expr, ctx)
        ast.enclosing_scope = ctx


def callstmt(ast: asts.CallStmt, ctx: symbols.Scope):
    callexpr(ast.call, ctx)


def printstmt(ast: asts.PrintStmt, ctx: symbols.Scope):
    expr(ast.expr, ctx)


def stmt(ast: asts.Stmt, ctx: symbols.Scope):
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
            error.error(f"stmt() not implemented for {type(ast)}", ast.span)


def funcdecl(ast: asts.FuncDecl, ctx: symbols.Scope):
    id(ast.id, ctx)
    symbolTable = {}
    # create the function scope
    scope = symbols.FuncScope(ctx, ast.span)
    scope.symtab = symbolTable
    ast.func_scope = scope
    for param in ast.params:
        newIdSymbol = symbols.IdSymbol(param.id.token.value, scope)
        name = param.id.token.value
        symbolTable[name] = newIdSymbol
        paramdecl(param, scope)
    typ(ast.ret_type_ast, scope)
    compoundstmt(ast.body, scope)


def program(ast: asts.Program):
    scope = symbols.GlobalScope(ast.span)
    symTab = {}
    scope.symtab = symTab
    for decl in ast.decls:
        newIdSymbol = symbols.IdSymbol(decl.id.token.value, scope)
        if decl.id.token.value == "main":
            if decl.id.token.value in symTab:
                error.error("main function already declared", decl.id.span)
        symTab[decl.id.token.value] = newIdSymbol
        funcdecl(decl, scope)
    
    
