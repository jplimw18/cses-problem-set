from pathlib import Path
import sys
import subprocess


PROBLEM_PATH_EXPECTED = "Path with tests/ and solution.py is required."
ARGUMENT_IS_NOT_DIR = "The argument is not a valid dir."
TESTS_DIR_NOT_FOUND = "tests/ dir not found."
SOLUTION_FILE_NOT_FOUND = "solution.py file not found."
INVALID_SOLUTION_FILE = "solution must be .py."
TESTS_DIR_EMPTY = "No .in files found in tests/."

DEFAULT_TEST_DIR_NAME = "tests"
DEFAULT_SLN_NAME = "solution.py"


def normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def run_solution(input_data: str, solution_path: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(solution_path)],
        input=input_data,
        text=True,
        capture_output=True,
        timeout=2
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout


def main():
    if len(sys.argv) <= 1:
        raise ValueError(PROBLEM_PATH_EXPECTED)

    problem_path = Path(sys.argv[1])

    if not problem_path.exists() or not problem_path.is_dir():
        raise NotADirectoryError(ARGUMENT_IS_NOT_DIR)

    tests_path = problem_path / DEFAULT_TEST_DIR_NAME

    if not tests_path.exists() or not tests_path.is_dir():
        raise FileNotFoundError(TESTS_DIR_NOT_FOUND)

    solution_file = problem_path / DEFAULT_SLN_NAME

    if not solution_file.exists() or not solution_file.is_file():
        raise FileNotFoundError(SOLUTION_FILE_NOT_FOUND)

    if solution_file.suffix != ".py":
        raise TypeError(INVALID_SOLUTION_FILE)

    in_files = sorted(tests_path.glob("*.in"))

    if not in_files:
        print(TESTS_DIR_EMPTY)
        return

    passed = 0
    total = len(in_files)

    for in_file in in_files:
        out_file = in_file.with_suffix(".out")

        if not out_file.exists():
            print(f"[SKIP] {in_file.name}: missing {out_file.name}")
            continue

        input_data = in_file.read_text()
        expected = out_file.read_text()

        try:
            actual = run_solution(input_data, solution_file)

            if normalize(actual) == normalize(expected):
                print(f"[OK] {in_file.name}")
                passed += 1
            else:
                print(f"[FAIL] {in_file.name}")
                print(f"Expected:\n{expected}\n")
                print(f"Actual:\n{actual}\n")

        except subprocess.TimeoutExpired:
            print(f"[TLE] {in_file.name}: time limit exceeded")

        except Exception as ex:
            print(f"[ERROR] {in_file.name}")
            print(ex)

    print(f"\nPassed {passed}/{total} tests")


if __name__ == "__main__":
    main()