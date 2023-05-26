---
title: CSC 453 Milestone 8
author: Todd Proebsting
---

# CSC 453 Milestone 8 (Typechecking)
[Revision 0: March 9, 2023]

## Due: Tuesday, March 28, 2023, @7pm

## Goal:
This milestone is to decorate/annotate an Tau AST with semantic types.  This phase directly follows creating symbol bindings.

## Specifications

The Tau language specification is a separate document.

The AST nodes are defined in `asts.py`.

Symbols and types are defined in `symbols.py`.


## Create `typecheck.py`

You will create a new file called `typecheck.py` that will contain the code for annotating the AST and Symbols with their semantic types.

To accomplish this, you will walk the AST built by your parser (after doing symbol binding):

Check `asts.py` for AST nodes that include a `semantic_type` field.  Similarly, check `symbols.py` for symbols that include a `semantic_type` field.


## Adapt `template.py` to create `typecheck.py`

The file `template.py` contains routines for walking the AST.  The routines do not do anything other than walk the tree, but they make a good starting point for your code.

I recommend copying `template.py` to `typecheck.py` and modifying it to do what you need.

## Your `scanner.py`, `parser.py`, and `bindings.py` should work

You will use the scanner, parser, and binder from previous milestones.

## Testing

I am providing a test program and test input.  More input will come as we get closer to the due date.

```
$ python3 testerator.py run --input tests.pickle
```

In the example above, `test.pickle` is the test input.  You can use this to test your code.

NOTE: The you can add `--verbose` and `--crash` flags to the command line to get more information about what is happening.

## Notes

The Tau language specification is a separate document.  It may not be complete.  If you have questions, please ask on Piazza.

Feel free to publically discuss the language specification on Piazza.  If you have questions, please ask.

## Type Errors

Your type checker should report type errors by throwing an exception with a meaningful error message.  This milestone will not explicitly check that you are doing this, but a later milestone will.

This milestone only requires that you correctly annotate a correct Tau program.

## Difficulty

This milestone does not require a lot of code beyond the tree walker, which is provided.  That said, it can be a little tricky to check and infer types for some nodes.

Start early and ask questions.

## Turning in the program

Turn in your program via Gradescope.  You will need to submit the following:

*  your parser in `parser.py`
*  your scanner in `scanner.py`
* your bindings code in `bindings.py`
* your type checking code in `typecheck.py`

## Grading

If your submission passes at least 80% of the test cases, you will get full credit for this milestone.

