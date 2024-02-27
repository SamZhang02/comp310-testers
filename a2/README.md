# Student Made Assignment 2 Tests

This is a repository of student made tests for COMP310 assignment 2, Winter 2024.

## Prerequisites

You must first make a copy of your assignment 2 codebase, including the Makefile into the current directory, under a directory called `./src`.

This is important, because we need to be able to build with dynamic macros with your Makefile.

## Runing the tests

To run the tests, you should start by mounting the assignment 2 repository a docker container. You can do this by running the following command:

```bash
make docker
```

You can then run the tests by running the following command:

```bash
python3 test.py
```

The tests by default do not show any output. If you want to see the output of the tests, you can run add following flag:

```bash
python3 test.py -v
```

or

```bash
python3 test.py -verbose
```

## Contributing

Contributions are welcome.

The main entry point of the test is `test.py`, where there is a client class to help with testing.

Individuals tests should be defined in the dictionary `tests`, where each test is a directory, including a `config.json` file to define the test's name, input command file path and the output file path to compare the stdout to, and compile-time macros. The directory also the input file, output file, and other files that are necessary for the test.

**IMPORTANT**: This test does **not** test at a unit level, it tests the shell in an end-to-end way and only performs assertions on stdout. Your program **must** quit at the end by using `quit` or some kind of interrupt, otherwise, the test suite will hang.

## Disclaimer

This test does not guarantee correctness.

This test is purely student-made and is not responsible for any inaccuracy with the official tests.
