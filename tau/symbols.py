from typing import Set, List, Dict, Tuple, Optional
from .tokens import Span


class SemanticType:
    def __eq__(self, other: "SemanticType") -> bool:
        assert False, "not implemented"

    def size(self) -> int:
        assert False, f"{type(self)}.size() not implemented"


class VoidType(SemanticType):
    def size(self) -> int:
        return 0

    def __eq__(self, other: SemanticType) -> bool:
        return isinstance(other, VoidType)


class IntType(SemanticType):
    def __eq__(self, other: SemanticType) -> bool:
        return isinstance(other, IntType)

    def size(self) -> int:
        return 1


class BoolType(SemanticType):
    def __eq__(self, other: SemanticType) -> bool:
        return isinstance(other, BoolType)

    def size(self) -> int:
        return 1


class ArrayType(SemanticType):
    def __init__(self, element_type: SemanticType):
        self.element_type: SemanticType = element_type

    def __eq__(self, other: SemanticType) -> bool:
        if isinstance(other, ArrayType):
            return self.element_type == other.element_type
        return False


class PhonyType(SemanticType):
    def __eq__(self, other: SemanticType) -> bool:
        return isinstance(other, PhonyType)


class FuncType(SemanticType):
    def __init__(self, params, ret: SemanticType):
        self.params: list[SemanticType] = params
        self.ret: SemanticType = ret
        self.param_size: int = 0
        self.frame_size: int = 0

    def __eq__(self, other: SemanticType) -> bool:
        return (
            isinstance(other, FuncType)
            and self.params == other.params
            and self.ret == other.ret
        )


class Symbol:
    offset: int = 0

    def __eq__(self, other: "Symbol") -> bool:
        assert False, f"not implemented for {type(self)}"

    def set_type(self, t: SemanticType) -> None:
        assert False, f"not implemented for {type(self)}"

    def get_type(self) -> SemanticType:
        assert False, f"not implemented for {type(self)}"


class IdSymbol(Symbol):
    def __init__(self, name: str, scope: "Scope"):
        self.name: str = name
        self.scope: Scope = scope
        self._semantic_type: SemanticType = PhonyType()

    def set_type(self, t: SemanticType):
        self._semantic_type = t

    def get_type(self) -> SemanticType:
        return self._semantic_type

    def __eq__(self, other: "Symbol") -> bool:
        return (
            isinstance(other, IdSymbol)
            and self.name == other.name
            # and self.semantic_type == other.semantic_type
            and self.scope.depth() == other.scope.depth()
            # and self.scope == other.scope # not checked to avoid infinite recursion
        )

    def __repr__(self):
        return "Symbol(%r, %r)" % (self.name, self._semantic_type)


class PhonySymbol(Symbol):
    def __init__(self):
        pass

    def __eq__(self, other: "Symbol") -> bool:
        return isinstance(other, PhonySymbol)


class Scope:
    symtab: dict[str, Symbol]
    parent: Optional["Scope"]
    span: Span

    def lookup(self, name: str) -> Symbol | None:
        if name in self.symtab:
            return self.symtab[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def __eq__(self, other: "Scope") -> bool:
        assert False, f"not implemented for {type(self)}"

    def depth(self) -> int:
        if self.parent:
            return self.parent.depth() + 1
        return 0


# holds parameters
class FuncScope(Scope):
    def __init__(self, parent, span: Span):
        self.symtab = {}
        self.parent = parent
        self.span = span

    def __eq__(self, other: Scope) -> bool:
        return (
            isinstance(other, FuncScope)
            and self.symtab == other.symtab
            and self.parent == other.parent
        )


# holds symbols in compound statement
class LocalScope(Scope):
    def __init__(self, parent, span: Span):
        self.parent: Scope = parent
        self.span: Span = span
        self.symtab: dict[str, Symbol] = {}

    def __eq__(self, other: Scope) -> bool:
        return (
            isinstance(other, LocalScope)
            and self.symtab == other.symtab
            and self.parent == other.parent
        )


# holds global symbols (i.e., function declarations)
class GlobalScope(Scope):
    def __init__(self, span: Span):
        self.span: Span = span
        self.symtab: dict[str, Symbol] = {}
        self.parent = None

    def __eq__(self, other: Scope) -> bool:
        return isinstance(other, GlobalScope) and self.symtab == other.symtab


class PhonyScope(Scope):
    def __init__(self):
        self.symtab: dict[str, Symbol] = {}
        self.parent = None

    def __eq__(self, other: Scope) -> bool:
        return isinstance(other, PhonyScope) and self.symtab == other.symtab
