import pprint
import argparse
import pickle
import contextlib
import io
import json
import pprint
import sys
from typing import Callable, Tuple, Any, Optional, Dict, NamedTuple, List

from .testers import *


class TestResult(NamedTuple):
    retval: Any
    out: io.StringIO
    err: io.StringIO
    exc: Optional[Exception]


def print_test(result: TestResult, test: Dict):
    print(f"file: {test['file']}")
    print(f"input: {test['input']}")
    print(f"expected return value: {test['output']}")
    print(f"actual return value: {result.retval}")
    print(f"expected stdout: {test['stdout']}")
    print(f"stdout: {result.out.getvalue()}")
    print(f"expected stderr: {test['stderr']}")
    print(f"stderr: {result.err.getvalue()}")
    if result.exc is not None:
        print(f"exception: {result.exc}")


def print_result(result: TestResult):
    print(f"actual return value:")
    pprint.pprint(result.retval)
    print(f"stdout: {result.out.getvalue()}")
    print(f"stderr: {result.err.getvalue()}")
    if result.exc is not None:
        print(f"exception: {result.exc}")


def get_function(name: str) -> Callable:
    names = name.split(".")  # e.g. "foo.bar.baz"
    fn = globals()[names[0]]
    for name in names[1:]:
        fn = getattr(fn, name)
    return fn


def run_limited(fn, input):
    limit = 100000000

    def limiter(a, b, c):
        nonlocal limit
        limit -= 1
        if limit == 0:
            raise Exception("Time limit exceeded")
        return limiter

    sys.settrace(limiter)
    student = fn(input)
    sys.settrace(None)
    return student


def run_test(
    input: str, funcname: str, verbose: bool, crash: bool
) -> TestResult:
    out = io.StringIO()
    err = io.StringIO()
    try:
        fn = get_function(funcname)
        with contextlib.redirect_stdout(out):
            with contextlib.redirect_stderr(err):
                student = run_limited(fn, input)
        return TestResult(student, out, err, None)
    except Exception as e:
        if crash:
            raise
        return TestResult(None, out, err, e)


def evaluate_test(
    test: Dict, verbose: bool, crash: bool
) -> Tuple[bool, TestResult]:
    compare = get_function(test["compare"])
    result: TestResult = run_test(
        test["input"], test["function"], verbose, crash
    )
    try:
        res = compare(result.retval, test["output"], crash)
    except Exception as e:
        if crash:
            raise
        res = False
    return (
        (
            result.exc is None
            and res
            and result.out.getvalue() == test["stdout"]
            and result.err.getvalue() == test["stderr"]
        ),
        result,
    )


def run(
    filenames: List[str],
    verbose: bool,
    crash: bool,
    allOrNothing=None,
    name=None,
) -> Dict:
    if verbose:
        print("Running tests")
    gradescope = {
        "score": 0,
        "output": "",
        "visibility": "visible",
        "tests": [],
    }
    correct = 0
    total = 0
    for filename in filenames:
        if verbose:
            print(f"Reading {filename}")
        with open(filename, "rb") as f:
            tests: List[Dict] = pickle.load(f)
        for test in tests:
            if name is not None and test["file"] != name:
                continue
            if verbose:
                pprint.pprint(test)
            passed: bool
            result: TestResult
            passed, result = evaluate_test(test, verbose, crash)
            if verbose:
                print(f"passed: {passed}")
                print_result(result)
                print("-----")
            gradescope_test = {
                "status": "passed" if passed else "failed",
                "name": test["file"],
            }
            if passed:
                correct += 1
            gradescope["tests"].append(gradescope_test)

        total += len(tests)
    gradescope["output"] = f"{correct} / {total} correct"
    ratio: float = correct / total
    if allOrNothing is not None:
        if ratio >= allOrNothing:
            gradescope["score"] = 100
        else:
            gradescope["score"] = 0
    else:
        gradescope["score"] = 100 * correct / total
    return gradescope


def do_gradescope(filenames: List[str], outfile: str, allOrNothing=None):
    gradescope = run(filenames, False, False, allOrNothing)
    j = json.dumps(gradescope, indent=2)
    with open(outfile, "w") as f:
        f.write(j)


def process_test_inputs(
    compare_name, fn_name, file_name, input: Any, verbose
) -> Dict:
    result = run_test(input, fn_name, verbose, False)
    test = {
        "file": file_name,
        "function": fn_name,
        "compare": compare_name,
        "input": input,
        "output": result.retval,
        "stdout": result.out.getvalue(),
        "stderr": result.err.getvalue(),
        "error": result.exc,
    }
    return test


def read_input(args, input) -> list[str]:
    if args.verbose:
        print(f"Reading {input}")
    if args.pickle:
        with open(input, "rb") as f:
            tests = pickle.load(f)
    elif args.json:
        with open(input, "r") as f:
            tests = json.load(f)
    elif args.text:
        with open(input, "r") as f:
            tests = [f.read()]
    else:
        assert False
    return tests


def create(args):
    outputs = []
    for fname in args.input:
        tests = read_input(args, fname)
        for input in tests:
            output = process_test_inputs(
                args.compare,
                args.function,
                fname,
                input,
                args.verbose,
            )
            outputs.append(output)
    if args.verbose:
        print(f"Writing output.  {len(outputs)} tests")
    with open(args.output, "wb") as f:
        pickle.dump(outputs, f)


def main():
    args = parse_args()
    match args.command:
        case "create":
            create(args)
        case "run":
            results = run(
                args.input,
                args.verbose or args.crash,
                args.crash,
                None,
                args.name,
            )
            pprint.pprint(results, indent=4, sort_dicts=False)
        case _:
            assert False


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="create a test pickle")
    create.add_argument("input", type=str, nargs="+", help="input file(s)")
    create.add_argument(
        "--output", type=str, required=True, help="output file"
    )
    create.add_argument(
        "--function", type=str, required=True, help="function to test"
    )
    create.add_argument(
        "--compare", type=str, required=True, help="comparison function"
    )
    create.add_argument(
        "--verbose", action="store_true", help="verbose output"
    )

    format = create.add_mutually_exclusive_group(required=True)
    format.add_argument(
        "--pickle", action="store_true", help="input is a pickle"
    )
    format.add_argument("--json", action="store_true", help="input is a json")
    format.add_argument(
        "--text", action="store_true", help="input is a text file"
    )

    run = subparsers.add_parser("run", help="run tests in a pickle file")
    run.add_argument("input", nargs="+", help="input test pickle file(s)")
    run.add_argument(
        "--verbose", action="store_true", help="enable verbose output"
    )
    run.add_argument("--crash", action="store_true", help="crash on error")
    run.add_argument(
        "--name", type=str, default=None, help="limit to a specific test"
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
