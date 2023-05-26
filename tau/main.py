import argparse
from typing import List


def main():
    args = get_args()
    fname = args.file
    with open(fname) as f:
        input = f.read()
    interpret(input, args.args, args.verbose, args.stopafter)


def interpret(input, args, verbose, stopafter):
    import scanner

    lexer = scanner.Scanner(input)
    if stopafter == "scanner":
        return
    import parse

    psr = parse.Parser(lexer)
    tree = psr.parse()
    if stopafter == "parser":
        return
    import bindings

    bindings.bind(tree)
    if stopafter == "bindings":
        return
    import typecheck

    typecheck.program(tree)
    if stopafter == "typecheck":
        return
    import offsets

    offsets.program(tree)
    if stopafter == "offsets":
        return
    import codegen

    insns = codegen.generate(tree)
    from tau.vm import vm_utils

    if verbose:
        vm_utils.dump_insns(insns)
    vm_utils.invoke_vm(insns, args, verbose)


def get_args():
    ap: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Compile Tau files"
    )
    ap.add_argument("--file", required=True, help="The file to compile")
    ap.add_argument(
        "--verbose",
        action="store_true",
        help="Cause the interpreter to be more verbose",
    )
    ap.add_argument("--stopafter", type=str, help="Stop after a certain phase")
    ap.add_argument(
        "args", nargs="*", help="Arguments to pass to the program as integers"
    )
    return ap.parse_args()


if __name__ == "__main__":
    main()
