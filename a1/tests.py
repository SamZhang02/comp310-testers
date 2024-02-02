import subprocess
import os
import shutil

class ShellTestClient:

  def __init__(self, shell_executable):
    self.shell_executable = shell_executable
    self.stdout = None
    self.stderr = None

  def run_shell_with_input(self, input_commands_file):
    command = f'./{self.shell_executable} < {input_commands_file}',

    # print(f"running command {command}")

    process = subprocess.Popen(
      command,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
      shell=True
    )

    self.stdout, self.stderr = process.communicate()

  def assess_output(self, expected_output_file):
    if self.stderr:
      # print(f"Your program returned an error: {self.stderr}")
      return False

    with open(expected_output_file ,'r') as fobj:
      expected_output = fobj.read()

    stdout_lines = self.stdout.strip().split('\n')
    expected_lines = expected_output.strip().split('\n')

    # print(self.stdout)
    # print(expected_output)

    i = 0
    if len(stdout_lines) != len(expected_lines):
      print(f"Different numbers of lines, {len(stdout_lines)} in stdout, {len(expected_lines)} expected")
      return False

    for stdout_line, expected_line in zip(stdout_lines, expected_lines):
      if stdout_line.strip() != expected_line.strip():
        print(f"Test failed for line: {i}")
        print(f"Expected: {expected_line}")
        print(f"Got: {stdout_line}")
        return False
      i += 1

    return True


COMMANDS_PATH = "commands"
OUTPUT_PATH = "outputs"

def run_test(name, input_file, output_file):
    client = ShellTestClient('myshell')

    client.run_shell_with_input(input_file)

    if client.assess_output(output_file) is False:
        print(f"{name} ------ \033[91mfailed\033[0m")
        return False
    else:
        print(f"{name} ------ \033[92mok\033[0m")
        return True


def clean_directories():
    assets_dir = "assets"
    keep_dir = 'keep'

    os.chdir(assets_dir)

    for item in os.listdir('.'):
        path = os.path.join('.', item)

        if item == keep_dir:
            continue

        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    os.chdir('..')



def main():
  tests: dict[str, tuple[str,str]] = {
    "Launch without error": ("launch.txt", "launch.txt"),
    "Set variables like the assignment instructions": ("set_1.txt", "set_1.txt"),
    "Error when setting empty variables and set number as variables": ("set_2.txt", "set_2.txt"),
    "Echo non-variable, empty variables, filled variables, numeric variable names": ("echo.txt", "echo.txt"),
    "mkdir empty, mkdir too many, mkdir new dir. touch 2 new files and ls": ("navigate_1.txt", "navigate_1.txt"),
    "navigate to existing directory, ls existing files": ("navigate_2.txt", "navigate_2.txt"),
    "nested cd": ("navigate_3.txt", "navigate_3.txt"),
    "empty_command": ("empty.txt", "empty.txt"),
    "nested mkdir": ("nest_mkdir.txt", "nest_mkdir.txt"),
    "nested touch, empty touch": ("touch.txt", "touch.txt"),
    "null cat, empty cat, long cat": ("meow.txt", "meow.txt"),
    "empty ls, normal ls": ("ls.txt", "ls.txt")
  }

  ok_count = 0
  for name, paths in tests.items():
    input = os.path.join(COMMANDS_PATH, paths[0])
    output = os.path.join(OUTPUT_PATH, paths[1])

    if run_test(name, input, output):
      ok_count += 1

    clean_directories()

  print(f"{len(tests)} tests ran, {ok_count} tests passed.")

if __name__ == "__main__":
  main()
