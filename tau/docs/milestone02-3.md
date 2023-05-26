---
title: CSC 453 Milestones 2 and 3
author: Todd Proebsting
geometry: "left=1.6cm,right=1.6cm,top=3cm,bottom=2cm"
output: pdf_document
fontsize: 12pt
---

# CSC 453 Milestones 2 (Partial Scanner) and 3 (Full Scanner)
[Revision 0: January 25, 2023]

## Due Dates:

* Milestone 2: Tuesday, January 31, 2023 at 7pm
* Milestone 3: Tuesday, February 7, 2023 at 7pm

## Goal:
These milestones is writing a scanner for Tau.  

## Specifications

1. The scanner is a class called `Scanner`.
2. The stubbed `Scanner` class is given in `tau/stubs/scanner.py`.  You will need to copy this file to your working directory and edit it.
3. The classes for tokens and coordinates is given in `tau/tokens.py`, which is provided for you.  You MUST NOT EDIT this file.
4. The syntax error reporting routine is given in `tau/error.py`, which is provided for you.  You MUST NOT EDIT this file.

## Tau Language Tokens

1. Identifiers are sequences of letters and digits that start with a letter. ('ID').  Letters are defined by Python's `string.ascii_letters` and digits are defined by Python's `string.digits`.
2. Tau includes many keywords.  Tokens returned for keywords will have the keyword as both the `kind` and the `value`.
2. Integer literals are sequences of digits. ('INT')
3. Tau's punctuation and operators are given in `tau/tokens.py`.
4. Skip over comments.  Comments start with `//` and go to the end of the line.
5. Skip over whitespace.  Whitespace is defined by Python's `string.whitespace`.
6. The scanner should return `Token("EOF", "", span)` when it reaches the end of the input string, where `span` is created with the coordinates where the end was reached for both beginning and end.

## Milestone 2 subset

Milestone 2 requires that you only handle the following:

* Scan identifiers
* Scan integer literals
* Skip whitespace
* Skip comments
* Return `Token("EOF", "", span)` when the end of the input is reached.
* Compute correct spans for tokens.

## Milestone 3 full scanner

Milestone 3 requires that you handle the entire language.

## Error Reporting

1. If the scanner encounters a character that is not part of the language, it should report an error using `error.error()`.  This will raise an exception that will terminate the program.
2. This milestone will not prescribe any particular error message for any particular error.  You are free to choose your own error messages.

## Standard Requirements

1. Use Python 3.10 as the implementation language
2. Use `black` to format your code.
3. Use `pyright` to check your code for type errors. Your code must be error- and warning-free
4. Turn the program in via Gradescope.
5. The program must meet the speciciations below.


## Restrictions

1. You may not use regular expressions to implement the scanner.
2. You may not use any external libraries to implement the scanner.
3. The intention is that you hand-code the scanner.  Please refrain from using shortcuts.  If you have questions, please ask.

## Turning in the program

Turn in your program via Gradescope.  You will need to submit a single Python file called `scanner.py`.

## Grading

If your submission passes at least 80% of the test cases, you will get full credit for this milestone.

## Comments

Comments in computer programs are meant to improve the readability of the program by somebody in the future.  Write comments accordingly.

* Too many, or too long, comments make the code harder to read.
* Too few, or too short, comments make the code harder to read.

Points will only be lost when comments are horrible.

## Programming Techiques

The hallmarks of good programming are simplicity, clarity and ease of understanding.  Programs in CSC 453 should be written to be understood by other people.  Clever techniques that obscure what the code is doing are strongly discouraged.

Good object-oriented programming is encouraged.  Bad OO programming is strongly discouraged.  Overuse of inheritance is a very clear sign of bad OO programming.

Programs may lose points for lack of clarity, simplicity, or ease of understanding.

