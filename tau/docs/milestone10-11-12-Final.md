---
title: CSC 453 Milestones 8-12
author: Todd Proebsting
---

# CSC 453 Milestones 10-12, and Final Project
[Revision 0: March 9, 2023]

[Revision 1: April 5, 2023: Fixed syntax in example code.]

## Due: Tuesday, April 12, -- May 2, 2023 @7pm

## Goal:

These milestones build the code generator for Tau in a series of steps until the whole project is finished.

### Common Interface to module `codegen`

```python
def generate(p: ast.Program) -> [Insn]:
    ...
```

The code generator will be implemented in the file `codegen.py`.


## Milestone 10: Due April 12 (Wednesday!)

Milestone 10 may be the hardest milestone.  Start early.

Milestone 10 will generate code for the following AST declaration, statement, and expression nodes:

* `Program(AST)`
* `FuncDecl(AST)`  (for m10, exclude parameter passing)
* `PrintStmt(Stmt)`
* `CompoundStmt(Stmt)` 
* `IntLiteral(Expr)`
* `IdExpr(Expr)` (for m10, only function names as identifiers)
* `BinaryOp(Expr)` (for m10, exclude short-circuit `and` and `or`)
* `UnaryOp(Expr)` (for m10, exclude `not`)

A complex program the compiler should handle for M8:

```
func main(): void {
    print 4 * 3 + -2 / (2+4)
    print true
}
```

Because this milestone excludes the ability to call functions, only `main()` can be called.


## Milestone 11: Due April 20 (Thursday!)

Milestone 9 will add the following:

* `ReturnStmt(Stmt)` (including return values)
* `IdExpr(Expr)` (include local variables)
* `CallStmt(Stmt)`
* `CallExpr(Expr)` (for m11, exclude parameter passing)
* `AssignStmt(Stmt)`
* `IfStmt(Stmt)`
* `WhileStmt(Stmt)`
* `BinaryOp(Expr)` (for m11, add short-circuit `and` and `or`)
* `UnaryOp(Expr)` (for m11, add `not`)

This milestone adds the ability to call functions, but not to pass parameters.

There will be no binary or unary expressions that include function calls in this milestone.  (You may want to test this anyway.)

## Milestone 12: Due April 27 (Thursday!)

Milestone 12 will add the following:

* `FuncDecl(AST)`  (include parameter passing)
* `CallExpr(Expr)` (include parameter passing)

This milestone adds parameter passing.

Like the previous milestone, there will be no binary or unary expressions that include function calls in this milestone.  (You may want to test this anyway.)


## Final Project: Due May 2

The final project will add the following:

* Binary and unary expressions that include function calls.  E.g.,
    * `print 4 * f(3) + -2 / (2+4)`
    * `print f(3) and g(4+3)`
    * `print not f(g(3)+h(4))`
    * `x = f(3) + g(f(4))`
* Better Error reporting (More details to come.)
* More test cases

## Specifications

The Tau language specification is a separate document.

## `main.py` controls compilation

The provided file `tau/main.py` will control the compilation process.  It will call the parser, the semantic analyzer, and the code generator.  It will also call the VM to execute the generated code.

Invocation is straightforward:

```
python3 -m tau.main.py --file source.tau
```

There is also a `--verbose` option that will cause the VM to print out the instructions as they are executed.

#### Calling Convention

The calling convention for Tau has been described in class.  This is a summary:

Caller Invocation:

* Caller put's outgoing arguments at negative offsets from its frame pointer.  (The first is at offset -2, the second at offset -3, etc.)
* Caller has an empty evaluation stack when it does the `Call` instruction. [optional]
* Caller uses `Call` instruction to call a function.
Caller Upon Return:
* Caller makes sure the return value is put at offset `-1` from the `FP/SP` stack if appropriate.  (See below.)


Callee Prologue:

* Callee saves its return address at offset 0 from its FP
* Callee saves its caller's FP at offset 1 from its FP
* Callee *may* save caller's SP at offset 2 from its FP, but is not obliged to do so.
* Callee allocates its own frame, adjusting the FP and SP as appropriate.
* Callee's FP **must** be equal to the caller's SP.

Callee Epilogue:

* Callee must restore the caller's FP and SP before returning.

Return Values:

* Your compiler **must** implement return values as follows:
    * At offset -1 from the caller's SP, which is offset -1 from the callee's FP.



## Notes

The Tau language specification is a separate document.  It may not be complete.  If you have questions, please ask on Piazza.

Feel free to publically discuss the language specification on Piazza.  If you have questions, please ask.

## Errors

The milestones only requires that you correctly annotate a correct Tau program.

## `codegen_template.py` is available

You may find `codegen_template.py` useful.  It contains a skeleton for the code generator.  It is not required, but it may be useful.

## Turning in the program

Turn in your program via Gradescope.  You will need to submit the following:

* your parser in `parser.py`
* your scanner in `scanner.py`
* your bindings code in `bindings.py`
* your type checking code in `typecheck.py`
* your offset code in `offsets.py`
* your code generator in `codegen.py`

## Grading

For milestones, if your submission passes at least 80% of the test cases, you will get full credit for the milestone.

The final project will be graded based on passing test cases as well as an examination of the code.  (I.e., there is no 80% rule for the final project.)

