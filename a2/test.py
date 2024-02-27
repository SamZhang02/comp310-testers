import subprocess
import os
import json
import argparse
import shutil

ROOT = os.getcwd()
CODE_PATH = os.path.join(".", "src")


class Shell:

    def __init__(self, shell_executable, verbose):
        self.shell_executable = shell_executable
        self.stdout = ""
        self.stderr = ""
        self.verbose = verbose

    @classmethod
    def make_shell(cls, test, verbose=False):

        if os.path.exists(os.path.join(".", "myshell")):
            command = f"make clean && make myshell framesize={test.framesize} varmemsize={test.varmemsize}"
        else:
            command = (
                f"make myshell framesize={test.framesize} varmemsize={test.varmemsize}"
            )

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        _, stderr = process.communicate()

        if stderr:
            print(
                f"Error while building the shell, is your makefile correct?\nError message: {stderr}"
            )

            return None

        return cls(f"./myshell", verbose)

    def batch_run(self, input_commands_file) -> None:

        print(f"==============================================================")
        print(f"input content:")
        with open(input_commands_file, "r") as f:
            print(f.read())

        command = (f"{self.shell_executable} < {input_commands_file}",)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        self.stdout, self.stderr = process.communicate()

    def assert_output(self, expected_output_file) -> bool:

        with open(expected_output_file, "r") as fobj:
            expected_output = fobj.read()

        stdout_lines = [line for line in self.stdout.strip().split("\n") if line.strip() != ""]
        expected_lines = expected_output.strip().split("\n")

        i = 0
        if len(stdout_lines) != len(expected_lines):
            if self.verbose:
                print(f"We expected: {expected_output}")
                print(f"But your shell printed: {self.stdout}")

            print(f"Your shell printed this to stderr: {self.stderr}")
            return False

        for stdout_line, expected_line in zip(stdout_lines, expected_lines):
            if stdout_line.strip() != expected_line.strip():
                if self.verbose:
                    print(f"We expected: {expected_output}")
                    print(f"But your shell printed: {self.stdout}")

                print(f"Your shell printed this to stderr: {self.stderr}")
                return False
            i += 1

        return True


class Test:

    def __init__(self, dir, name, input, output, framesize, varmemsize):
        self.name = name
        self.dir = dir
        self.input = input
        self.output = output
        self.framesize = framesize
        self.varmemsize = varmemsize

    def run_with(self, client: Shell):
        # copy all files in the test directory to the current directory
        for file in os.listdir(self.dir):
            filepath = os.path.join(self.dir, file)
            shutil.copy(filepath, os.getcwd())

        client.batch_run(self.input)

        # remove all files but files needed for compilation
        os.system(
            r"find . -type f ! \( -name '*.c' -o -name '*.o' -o -name 'Makefile' -o -name '*.h' \) -delete"
        )

        if client.assert_output(self.output) is False:
            print(f"{self.name} ------ \033[91mfailed\033[0m")
            return False
        else:
            print(f"{self.name} ------ \033[92mok\033[0m")
            return True


TESTS_PATH = os.path.join(os.getcwd(), "tests")


def load_tests():
    tests = []
    for test_dir in os.listdir(TESTS_PATH):
        dir = os.path.join(TESTS_PATH, test_dir)

        if not os.path.isfile(os.path.join(dir, "config.json")):
            continue

        info = ""
        with open(os.path.join(dir, "config.json"), "r") as f:
            info = json.load(f)

        name = info["name"]
        input = os.path.join(dir,info["input"])
        output = os.path.join(dir,info["output"])
        framesize = info["macros"]["framesize"]
        varmemzsize = info["macros"]["varmemsize"]

        test = Test(dir, name, input, output, framesize, varmemzsize)
        tests.append(test)

    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        "-v",
        help="Show test expected output and user given output",
        action="store_true",
    )
    parser.add_argument(
        "--skip-public",
        help="Skip public tests",
        action="store_true",
    )
    args = parser.parse_args()

    os.chdir(CODE_PATH)

    tests = load_tests()

    tests_passed = 0
    tests_ran = 0
    tests_skipped = 0
    for test in tests:
        if args.skip_public and "public" in test.dir:
            continue

        client = Shell.make_shell(test, args.verbose)

        if client is None:
            print(f"{test.name} ------ \033[93mnot ran\033[0m")
            tests_skipped += 1
            continue

        err = test.run_with(client)
        tests_passed += 1 if err else 0
        tests_ran += 1

    print(f"==============================================================")
    print(f"Ran {tests_ran} tests\t\t {tests_passed} passed\t\t {tests_skipped} skipped")

    return 0


if __name__ == "__main__":
    err_code = main()
    exit(err_code)
