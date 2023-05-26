---
title: CSC 453 Milestone 7
author: Todd Proebsting
---

# CSC 453 Milestone 8 (Bindings)
[Revision 0: March 9, 2023]

## Due: Tuesday, March 21, 2023, @7pm

## Goal:
This milestone is to decorate/annotate an Tau AST with symbols.

## Specifications

The Tau language specification is a separate document.

The AST nodes are defined in `asts.py`.


## Create `bindings.py`

You will create a new file called `bindings.py` that will contain the code for binding `Id` nodes to their symbols.

To accomplish this, you will walk the AST built by your parser:

* Your program must create, enter, and leave scopes as needed.  This is done using routines in `symbols.py`.
* Your program will create symbols for newly declared names.
    * Newly created symbols must be added to the current scope's symbol table.
    * Your program will bind `Id` nodes to their symbols.

Study `symbols.py` to understand how to use it.

## Entry Point

The entry point for your code is the `bind` function in `bindings.py`.  This function takes an AST node as an argument and returns the same AST node.  The function will decorate the AST with symbols.

```
def bind(ast: asts.Program):
    # ...your code here...
    return ast
```

## Adapt `template.py` to create `bindings.py`

The file `tau/stubs/template.py` contains general-purpose routines for walking the AST.  The routines do not do anything other than walk the tree, but they make a good starting point for your code.

I recommend copying `template.py` to `bindings.py` and modifying it to do what you need.

## Your `scanner.py` and `parser.py`

You will use the scanner and parser from previous milestones.


## Testing

I am providing a test program and test input.  More input will come as we get closer to the due date.

```
$ python3 testerator.py run --input tau/m7/tests.pickle
```

In the example above, the pickle file is the test input.  You can use this to test your code.

NOTE: The you can add a `--verbose` flag to the command line to get more information about what is happening.

## Notes

The Tau language specification is a separate document.  It may not be complete.  If you have questions, please ask on Piazza.

Feel free to publically discuss the language specification on Piazza.  If you have questions, please ask.


## Difficulty

This milestone does not require a lot of code beyond the tree walker, which is provided.  That said, it can be a little tricky to create and remove scopes at the right times.

Start early and ask questions.

## Turning in the program

Turn in your program via Gradescope.  You will need to submit the following:

*  your parser in `parser.py`
*  your scanner in `scanner.py`
* your bindings code in `bindings.py`

## Grading

If your submission passes at least 80% of the test cases, you will get full credit for this milestone.

