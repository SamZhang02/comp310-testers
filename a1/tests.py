import subprocess
import os

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
      print(f"Your program returned an error: {self.stderr}")
      return False

    with open(expected_output_file ,'r') as fobj:
      expected_output = fobj.read()

    stdout_lines = self.stdout.strip().split('\n')
    expected_lines = expected_output.strip().split('\n')

    # print(stdout_lines)
    # print(expected_lines)

    for stdout_line, expected_line in zip(stdout_lines, expected_lines):
      if stdout_line.strip() != expected_line.strip():
        print(f"Test failed for line: {stdout_line}")
        print(f"Expected: {expected_line}")
        print(f"Got: {stdout_line}")
        return False

    return True


client = ShellTestClient('myshell')

COMMANDS_PATH = "./commands"
OUTPUT_PATH = "./outputs"

def run_test(name, input_file, output_file):
    client.run_shell_with_input(input_file)

    if client.assess_output(output_file) is False:
        print(f"{name} ------ \033[91mfailed\033[0m")
        return False
    else:
        print(f"{name} ------ \033[92mok\033[0m")
        return True

def main():
  tests: dict[str, tuple[str,str]] = {
    "Should launch without error": ("launch.txt", "launch.txt")
  }

  ok_count = 0
  for name, paths in tests.items():
    input = os.path.join(COMMANDS_PATH, paths[0])
    output = os.path.join(OUTPUT_PATH, paths[1])

    if run_test(name, input, output):
      ok_count += 1

  print(f"{len(tests)} tests ran, {ok_count} tests passed.")

if __name__ == "__main__":
  main()
