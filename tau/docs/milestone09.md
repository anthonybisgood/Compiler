---
title: CSC 453 Milestone 9
author: Todd Proebsting
---

# CSC 453 Milestone 9 (Offsets)
[Revision 0: March 9, 2023]

## Due: Tuesday, April 4, 2023, @7pm

## Goal:
This milestone is to decorate/annotate an Tau's variable and parameter symbols with their offsets. This phase directly follows typechecking.

## Specifications

The Tau language specification is a separate document.

The AST nodes are defined in `asts.py`.

Symbols and types are defined in `symbols.py`.


## Create `offsets.py`

You will create a new file called `offsets.py` that will contain the code for annotating the AST and Symbols with computed offsets.

To accomplish this, you will walk the AST built by your parser (after doing typechecking).

Specifically you will need to:
* Update the `offset` field of Symbols that represent local variables and parameters.  Assume that all `int` and `bool` values have unit (`1`) size.
* Update the `size` field of the `FuncDecl` AST node to be the total size of the local variablels **AND** the 3 extra slots for the return address, old frame pointer, and old stack pointer.  (Note that the parameters are **not** included in the size of the local variables.)
* The local variables must be *packed* (no gaps) as described in class.
* Your compiler does not need to handle arrays.

**NOTE:** The parameter offsets will all be negative values relative to the `SP`/`FP`, but they will start at `-2`.  (The return value will be at offset `-1`)

Example:

```
func f(
    int x,    // -2
    int y,    // -3
    int z)    // -4
{  
    int a;    // 3
    {
        int b;    // 4
    }
    while true {
        int c;    // 4  <-- packed!!
        int d;    // 5
    }
}     // size = 6
```

## Adapt `template.py` to create `offsets.py`

The file `template.py` contains routines for walking the AST.  The routines do not do anything other than walk the tree, but they make a good starting point for your code.

I recommend copying `template.py` to `offsets.py` and modifying it to do what you need.

## Your `scanner.py`, `parser.py`, `bindings.py`, and `typecheck.py` should work

You will use the scanner, parser, binder, and typechecker from previous milestones.


## Testing

I will be providing a test program and test input.  More input will come as we get closer to the due date.

```
$ python3 testerator.py run --input test.pickle
```

In the example above, `test.pickle` is the test input.  You can use this to test your code.

NOTE: The you can add a `--verbose` flag to the command line to get more information about what is happening.

NOTE: There is a new `--crash` flag that will cause the testerator to throw an exception if it encounters an error.  This is useful for debugging.

## Notes

The Tau language specification is a separate document.  It may not be complete.  If you have questions, please ask on Piazza.

Feel free to publically discuss the language specification on Piazza.  If you have questions, please ask.

## Errors

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
* your offset code in `offsets.py`

## Grading

If your submission passes at least 80% of the test cases, you will get full credit for this milestone.

