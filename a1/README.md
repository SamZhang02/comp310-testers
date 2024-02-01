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

Individuals tests should be defined inside functions, which are stored in a list in the main function

```
run_tests()
```

Input commands files are stored under `/commands` and output files to compare to are stored in `/outputs`.

## Disclaimer
This test is does not guarantee correctness.
This test purely student-made is not responsible for any innacuracy with the official tests.

