from tau import asts, symbols, error


# process is the entry point for the visitor
# It may need to be renamed to match the name of the pass
def process(ast: asts.Program):
    program(ast)


def id(ast: asts.Id, retType: symbols.SemanticType):
    ast.semantic_type = ast.symbol.get_type()


def idexpr(ast: asts.IdExpr, retType: symbols.SemanticType):
    id(ast.id, retType)
    ast.semantic_type = ast.id.semantic_type


def callexpr(ast: asts.CallExpr, retType: symbols.SemanticType):
    expr(ast.fn, retType)
    if isinstance(ast.fn.semantic_type, symbols.FuncType):
        ast.semantic_type = ast.fn.semantic_type.ret
        if len(ast.args) != len(ast.fn.semantic_type.params):
            error.error(f"Wrong number of arguments for function {ast.fn}", ast.span)
    for arg in ast.args:
        expr(arg, retType)


def arraycell(ast: asts.ArrayCell, retType: symbols.SemanticType):
    expr(ast.arr, retType)
    expr(ast.idx, retType)
    if ast.idx.semantic_type != symbols.IntType():
        error.error("Array index must be int", ast.idx.span)
    ast.semantic_type = symbols.IntType()


def intliteral(ast: asts.IntLiteral, retType: symbols.SemanticType):
    ast.semantic_type = symbols.IntType()


def boolliteral(ast: asts.BoolLiteral, retType: symbols.SemanticType):
    ast.semantic_type = symbols.BoolType()


def binaryop(ast: asts.BinaryOp, retType: symbols.SemanticType):
    expr(ast.left, retType)
    expr(ast.right, retType)
    if ast.op.value in {"+", "-", "*", "/"}:
        if ast.left.semantic_type != symbols.IntType():
            error.error("Binary operation is valid for int only", ast.left.span)
        elif ast.right.semantic_type != symbols.IntType():
            error.error("Binary operation is valid for int only", ast.right.span)
        ast.semantic_type = symbols.IntType()
    elif ast.op.value in {"<", ">", "<=", ">=", "==", "!=", "and", "or"}:
        if ast.op.value in {"<", ">", "<=", ">=", "==", "!="}:
            if ast.left.semantic_type != ast.right.semantic_type:
                error.error("Binary operation is valid for same types only", ast.span)
        if ast.op.value in {"and", "or"}:
            if ast.left.semantic_type != symbols.BoolType():
                error.error("Binary operation is valid for bool only", ast.left.span)
            elif ast.right.semantic_type != symbols.BoolType():
                error.error("Binary operation is valid for bool only", ast.right.span)
        if ast.left.semantic_type != ast.right.semantic_type:
            error.error("Binary operation is valid for same types only", ast.span)
        ast.semantic_type = symbols.BoolType()


def unaryop(ast: asts.UnaryOp, retType: symbols.SemanticType):
    expr(ast.expr, retType)
    if ast.op.value in {"-"}:
        ast.semantic_type = symbols.IntType()
    elif ast.op.value in {"not"}:
        ast.semantic_type = symbols.BoolType()


def expr(ast: asts.Expr, retType: symbols.SemanticType):
    match ast:
        case asts.IdExpr():
            idexpr(ast, retType)
        case asts.CallExpr():
            callexpr(ast, retType)
        case asts.ArrayCell():
            arraycell(ast, retType)
        case asts.IntLiteral():
            intliteral(ast, retType)
        case asts.BoolLiteral():
            boolliteral(ast, retType)
        case asts.BinaryOp():
            binaryop(ast, retType)
        case asts.UnaryOp():
            unaryop(ast, retType)
        case _:
            errorMsg = f"expr() not implemented for {type(ast)}"
            error.error(errorMsg, ast.span)


def inttype(ast: asts.IntType, retType: symbols.SemanticType):
    ast.semantic_type = symbols.IntType()


def booltype(ast: asts.BoolType, retType: symbols.SemanticType):
    ast.semantic_type = symbols.BoolType()


def arraytype(ast: asts.ArrayType, retType: symbols.SemanticType):
    if ast.size is not None:
        expr(ast.size, retType)
    # check if size is int
    if ast.size != None and ast.size.semantic_type != symbols.IntType():
        error.error("Array size must be int", ast.size.span)
    if typ(ast.element_type_ast, retType) == -1:
        error.error("Array element type must be int or bool", ast.span)
    ast.semantic_type = symbols.ArrayType(ast.element_type_ast.semantic_type)


def voidtype(ast: asts.VoidType, retType: symbols.SemanticType):
    ast.semantic_type = symbols.VoidType()


def typ(ast: asts.TypeAST, retType: symbols.SemanticType) -> int:
    match ast:
        case asts.IntType():
            inttype(ast, retType)
        case asts.BoolType():
            booltype(ast, retType)
        case asts.ArrayType():
            arraytype(ast, retType)
        case asts.VoidType():
            voidtype(ast, retType)
        case _:
            return -1
    return 0


def paramdecl(ast: asts.ParamDecl, retType: symbols.SemanticType):
    id(ast.id, retType)
    if typ(ast.type_ast, retType) == -1:
        error.error("Parameter type must be int or bool", ast.span)
    ast.id.semantic_type = ast.type_ast.semantic_type
    ast.id.symbol.set_type(ast.id.semantic_type)
    ast.semantic_type = ast.type_ast.semantic_type


def vardecl(ast: asts.VarDecl, retType: symbols.SemanticType):
    id(ast.id, retType)
    if typ(ast.type_ast, retType) == -1:
        error.error("Variable type must be int or bool", ast.span)
    ast.id.semantic_type = ast.type_ast.semantic_type
    ast.id.symbol.set_type(ast.id.semantic_type)
    ast.semantic_type = ast.type_ast.semantic_type


def compoundstmt(ast: asts.CompoundStmt, retType: symbols.SemanticType):
    for decl in ast.decls:
        vardecl(decl, retType)
        decl.semantic_type = decl.type_ast.semantic_type
    for s in ast.stmts:
        stmt(s, retType)


def assignstmt(ast: asts.AssignStmt, retType: symbols.SemanticType):
    expr(ast.lhs, retType)
    expr(ast.rhs, retType)
    if ast.lhs.semantic_type != ast.rhs.semantic_type:
        error.error("Assign type mismatch", ast.lhs.span)


def ifstmt(ast: asts.IfStmt, retType: symbols.SemanticType):
    expr(ast.expr, retType)
    if ast.expr.semantic_type != symbols.BoolType():
        error.error("If condition must be bool", ast.expr.span)
    stmt(ast.thenStmt, retType)
    if ast.elseStmt is not None:
        stmt(ast.elseStmt, retType)


def whilestmt(ast: asts.WhileStmt, retType: symbols.SemanticType):
    expr(ast.expr, retType)
    if ast.expr.semantic_type != symbols.BoolType():
        error.error("While condition must be bool", ast.expr.span)
    stmt(ast.stmt, retType)


def returnstmt(ast: asts.ReturnStmt, retType: symbols.SemanticType):
    if ast.expr is not None:
        expr(ast.expr, retType)
        if ast.expr.semantic_type != retType:
            error.error("Return type mismatch", ast.expr.span)


def callstmt(ast: asts.CallStmt, retType: symbols.SemanticType):
    callexpr(ast.call, retType)


def printstmt(ast: asts.PrintStmt, retType: symbols.SemanticType):
    expr(ast.expr, retType)


def stmt(ast: asts.Stmt, retType: symbols.SemanticType):
    match ast:
        case asts.CompoundStmt():
            compoundstmt(ast, retType)
        case asts.AssignStmt():
            assignstmt(ast, retType)
        case asts.IfStmt():
            ifstmt(ast, retType)
        case asts.WhileStmt():
            whilestmt(ast, retType)
        case asts.ReturnStmt():
            returnstmt(ast, retType)
        case asts.CallStmt():
            callstmt(ast, retType)
        case asts.PrintStmt():
            printstmt(ast, retType)
        case _:
            errorMsg: str = f"stmt() not implemented for {type(ast)}"
            error.error(errorMsg, ast.span)


def funcdecl(ast: asts.FuncDecl, retType: symbols.SemanticType):
    id(ast.id, retType)
    params: list[symbols.SemanticType] = []
    for param in ast.params:
        paramdecl(param, retType)
        params.append(param.type_ast.semantic_type)
    if typ(ast.ret_type_ast, retType) == -1:
        error.error("Return type must be int or bool", ast.span)
    ast.id.semantic_type = symbols.FuncType(params, ast.ret_type_ast.semantic_type)
    ast.id.symbol.set_type(ast.id.semantic_type)
    compoundstmt(ast.body, ast.ret_type_ast.semantic_type)


def program(ast: asts.Program):
    for decl in ast.decls:
        funcdecl(decl, decl.ret_type_ast.semantic_type)
