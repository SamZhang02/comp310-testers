# Assignment 1 Tests

## Setup

1. Make a copy of your `./myshell` executable into this directory. This test repository will not build it for you.

2. You need to mount the same docker container as the assignment, you can use the command

```make
make docker
```

2. You can run the test within your docker container with

```make
make test
```

## Contributing

Contributions are welcome.

The main entry point of the test is `test.py`, where there is a client class to help with testing.

Individuals tests should be defined in the dictionary `tests`, which includes the same of the test, the input command file and the output file to compare the stdout to.

Input commands files are stored under `/commands` and output files to compare to are stored in `/outputs`.

any files created by your shell should be created in `./assets`, every file except `./assets/keep` created in this directory will be cleared after every test.

**IMPORTANT**: This test does **not** test at a unit level, it tests the shell in an end-to-end way and only performs assertions on stdout. Your program **must** quit at the end by using `quit` or some kind of interrupt, otherwise, the test suite will hang.

## Disclaimer

This test does not guarantee correctness.

This test is purely student-made and is not responsible for any innacuracy with the official tests.
