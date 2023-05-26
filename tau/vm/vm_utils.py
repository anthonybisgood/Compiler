from typing import List

from . import vm, vm_insns


def invoke_vm(insns, params, verbose):
    if verbose:
        dump_insns(insns)

    args = []
    for arg in reversed(params):
        if arg.isnumeric():
            args.append(int(arg))
        else:
            raise Exception(f"Invalid argument: {arg}")

    stack: List[int] = []
    memory: List[int] = args + [0] * 100000
    regs = {
        "PC": 0,
        "FP": 0,
        "SP": len(args) + 1,
    }
    exe = vm.Execution(insns, stack, memory, regs)
    exe.verbose = verbose
    exe.run()
    if (exe.regs["SP"] != len(args) + 1):
        raise Exception(f"Stack pointer not restored: {exe.regs}")
        assert exe.regs["SP"] == len(args) + 1


def dump_insns(insns):
    print("Instructions:")
    for i, insn in enumerate(insns):
        print(f"[{i:5}]", vm_insns.dis(insn, indent=8, long=False))
