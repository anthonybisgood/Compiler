A compiler for the Tau programming language. Based on Todd Proebsting's Compilers course at the University of Arizona.
Supports arithmetic, unary operations, type and scope checking, function calls, and precise error messages.  Runs on a virtual stack machine.
Users can write code that follows the language documentation.

Compiler is separated into 4 parts, the Scanner, Parser, Semantic Analysis, and Code Generation.

To Run:
Clone repository onto local machine, write your own *.tau file and use the command below to run.

python3 -m tau.main --file fileName.tau
