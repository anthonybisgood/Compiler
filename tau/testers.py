from typing import Callable, List, Any, Optional

from .tokens import Token
from .compare import assert_equal
from .error import CompilerError


def test_scanner(
    student: List[Token], expected: List[Token], crash: bool
) -> bool:
    try:
        return student == expected
    except:
        if crash:
            raise
        return False


def run_scanner(input: str) -> List[Token]:
    from scanner import Scanner

    lexer: Scanner = Scanner(input)
    tokens: List[Token] = []
    while lexer.peek().kind != "EOF":
        tokens.append(lexer.peek())
        lexer.consume()
    tokens.append(lexer.peek())
    return tokens


def test_generic(student: Any, expected: Any, crash: bool) -> bool:
    try:
        return student == expected
    except:
        if crash:
            raise
        return False


def test_pass(student: Any, expected: Any, crash: bool) -> bool:
    return True


def run_parser(input: str):
    from scanner import Scanner

    lexer: Scanner = Scanner(input)
    from parse import Parser

    psr: Parser = Parser(lexer)
    tree: Any = psr.parse()
    return None  # need to remove after m5


def test_ast(student: Any, expected: Any, crash: bool) -> bool:
    try:
        assert_equal(student, expected, lambda x, y: True)
        return True
    except:
        if crash:
            raise
        return False


def test_binding(student: Any, expected: Any, crash: bool) -> bool:
    from .asts import AST, Id, FuncDecl, CompoundStmt
    from .symbols import IdSymbol, FuncScope, LocalScope, Scope

    def bindings_checker(student: AST, expected: AST) -> bool:
        student_scope: Optional[Scope] = None
        expected_scope: Optional[Scope] = None
        match student:
            case Id():
                assert isinstance(
                    expected, Id
                ), f"{type(student)} != {type(expected)}"
                assert isinstance(
                    student.symbol, IdSymbol
                ), f"{type(student.symbol)} != {type(expected.symbol)}"
                assert isinstance(
                    expected.symbol, IdSymbol
                ), f"{type(student.symbol)} != {type(expected.symbol)}"
                assert (
                    student.symbol.name == expected.symbol.name
                ), f"{student.symbol.name} != {expected.symbol.name}"
                student_scope = student.symbol.scope
                expected_scope = expected.symbol.scope
            case FuncDecl():
                assert isinstance(
                    expected, FuncDecl
                ), f"{type(student)} != {type(expected)}"
                assert isinstance(
                    student.func_scope, FuncScope
                ), f"{type(student.func_scope)} != {type(expected.func_scope)}"
                assert isinstance(
                    expected.func_scope, FuncScope
                ), f"{type(student.func_scope)} != {type(expected.func_scope)}"
                student_scope = student.func_scope
                expected_scope = expected.func_scope
            case CompoundStmt():
                assert isinstance(
                    expected, CompoundStmt
                ), f"{type(student)} != {type(expected)}"
                assert isinstance(
                    student.local_scope, LocalScope
                ), f"{type(student.local_scope)} != {type(expected.local_scope)}"
                assert isinstance(
                    expected.local_scope, LocalScope
                ), f"{type(student.local_scope)} != {type(expected.local_scope)}"
                student_scope = student.local_scope
                expected_scope = expected.local_scope
            case _:
                pass
        while student_scope and expected_scope:
            assert (
                student_scope.span == expected_scope.span
            ), f"{student_scope.span} != {expected_scope.span}"
            assert type(student_scope) == type(
                expected_scope
            ), f"{type(student_scope)} != {type(expected_scope)}"
            student_scope = student_scope.parent
            expected_scope = expected_scope.parent
        assert student_scope is None, f"{student_scope} != None"
        assert expected_scope is None, f"{expected_scope} != None"
        return True

    try:
        v = test_ast(student, expected, crash)
        assert_equal(student, expected, bindings_checker)
        return v
    except:
        if crash:
            raise
        return False


def test_typecheck(student: Any, expected: Any, crash: bool) -> bool:
    from .asts import (
        AST,
        Id,
        FuncDecl,
        CompoundStmt,
        VarDecl,
        ParamDecl,
        Expr,
        TypeAST,
        Decl,
    )
    from .symbols import (
        IdSymbol,
        FuncScope,
        LocalScope,
        Scope,
        SemanticType,
        ArrayType,
        FuncType,
    )

    def assert_same_type(student: SemanticType, expected: SemanticType):
        assert type(student) == type(
            expected
        ), f"{type(student)} != {type(expected)}"
        if isinstance(expected, ArrayType):
            assert isinstance(student, ArrayType)
            assert_same_type(student.element_type, expected.element_type)
        if isinstance(expected, FuncType):
            assert isinstance(student, FuncType)
            assert_same_type(student.ret, expected.ret)
            assert len(student.params) == len(expected.params)
            for i in range(len(student.params)):
                assert_same_type(student.params[i], expected.params[i])

    def typecheck_checker(student: AST, expected: AST) -> bool:
        if isinstance(expected, Id):
            assert isinstance(student, Id)
            assert_same_type(student.semantic_type, expected.semantic_type)
            assert_same_type(
                student.symbol.get_type(), expected.symbol.get_type()
            )
        if isinstance(expected, Expr):
            assert isinstance(student, Expr)
            assert_same_type(student.semantic_type, expected.semantic_type)
        if isinstance(expected, TypeAST):
            assert isinstance(student, TypeAST)
            assert_same_type(student.semantic_type, expected.semantic_type)
        if isinstance(expected, Decl):
            assert isinstance(student, Decl)
            assert_same_type(student.semantic_type, expected.semantic_type)
        return True

    try:
        v = test_binding(student, expected, crash)
        assert_equal(student, expected, typecheck_checker)
        return v
    except:
        if crash:
            raise
        return False


def test_offsets(student: Any, expected: Any, crash: bool) -> bool:
    from .asts import (
        AST,
        Id,
    )
    from .symbols import (
        IdSymbol,
    )

    def offset_checker(student: AST, expected: AST) -> bool:
        if isinstance(expected, Id):
            assert isinstance(student, Id)
            if student.symbol.offset != expected.symbol.offset:
                print(student)
                print(expected)
            assert (
                student.symbol.offset == expected.symbol.offset
            ), f"{student.symbol.offset} != {expected.symbol.offset}"
        return True

    try:
        v = test_typecheck(student, expected, crash)
        assert_equal(student, expected, offset_checker)
        return v
    except:
        if crash:
            raise
        return False


def test_codegen(student: Any, expected: Any, crash: bool) -> bool:
    try:
        v = test_offsets(student, expected, crash)
        return v
    except:
        if crash:
            raise
        return False


def test_errors(student: Any, expected: Any, crash: bool) -> bool:
    return student == expected


def run_ast(input: str) -> Any:
    from scanner import Scanner

    lexer: Scanner = Scanner(input)
    from parse import Parser
    from .asts import Program

    psr: Parser = Parser(lexer)
    tree: Program = psr.parse()
    return tree


def run_binding(input: str):
    tree = run_ast(input)
    import bindings

    bindings.bind(tree)
    return tree


def run_typecheck(input: str):
    tree = run_binding(input)
    import typecheck

    typecheck.program(tree)
    return tree


def run_offsets(input: str):
    tree = run_typecheck(input)
    import offsets

    offsets.program(tree)
    return tree


def run_codegen(input: str):
    tree = run_offsets(input)
    import codegen
    from tau.vm import vm_utils
    from tau.vm.vm_insns import Insn

    insns: List[Insn] = codegen.generate(tree)
    
    vm_utils.invoke_vm(insns, [], False)
    return tree


def run_errors(input: str):
    try:
        tree = run_ast(input)
        import bindings

        bindings.bind(tree)
        import typecheck

        typecheck.program(tree)
        import offsets

        offsets.program(tree)
        import codegen

        codegen.generate(tree)
    except CompilerError as e:
        return "CompilerError"
    except Exception as e:
        return f"Other Error: {e}"
    return "<No error>"
