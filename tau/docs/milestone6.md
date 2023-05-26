---
title: CSC 453 Milestone 6
author: Todd Proebsting
date: 2022-02-22
---

# CSC 453 Milestone 6 (Build AST)
[Revision 0: February 22, 2022: Initial version]

## Due: Tuesday, March 14, at 7pm

## Goal:
This milestone is to build an AST for a syntactically correct Tau program.

## Specifications

The Tau language specification is a separate document.

The AST nodes are defined in `asts.py`.


## Editting your `parser.py`

You created a recursive descent parser in the previous milestone.  You will now modify your parser to build an AST.

When completed, the `Parser.parse()` method will return an AST.  It will return the root of the AST, which will have the type `asts.Program`.

## `scanner.py`

You will use the same scanner as previously.

## `tau/asts.py`

You will be given `asts.py`.  DO NOT MODIFY THIS FILE.  You will use the classes defined in this file to build your AST.


## Notes

The Tau language specification is intentionally vague.  Feel free to publically discuss the language specification on Piazza.  If you have questions, please ask.

Also, `asts.py` has scant comments.  Look at the initializers to understand them.

## Difficulty

Your grammar may not be the same as my grammar.  That's OK.  The goal is to get a working parser.  

That said, grammar writing can be tricky.  Start early and ask questions.

## Turning in the program

Turn in your program via Gradescope.  You will need to submit the following:

*  your parser in `parser.py`
*  your scanner in `scanner.py`

## Grading

If your submission passes at least 80% of the test cases, you will get full credit for this milestone.

