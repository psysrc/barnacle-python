# barnacle

An experimental interpreted programming language written in Python.

Aptly named because barnacles don't do a lot, are rough around the edges, and will cause you pain if you work with them too much.

## Build

This codebase makes use of Python 3.10 features.

### Standard build

1. Create a Python3 virtual environment with `python3 -m venv <venv name>`.
2. Activate the newly created virtual environment with `source <venv name>/bin/activate`.
3. Update pip with `pip install -U pip`.
4. Install dependencies with `pip install -U -r requirements.txt`.
5. Run `pip install .` to build and install the `barnacle` Python module.

### Developer build

Follow the "Standard build" instructions above, except when installing dependencies use `requirements-dev.txt` instead of `requirements.txt`.

#### Pylint Usage

1. Set `PYTHONPATH` with ``export PYTHONPATH=`pwd`/barnacle``.
2. Run pylint with `pylint barnacle/ test_barnacle/`.

#### Black Usage

1. Run black with `black .`.

#### isort Usage

1. Run isort with `isort .`.

#### Pytest Usage

1. Set `PYTHONPATH` with ``export PYTHONPATH=`pwd`/barnacle``.
2. Run pytest with `pytest`.

## Usage

Run `python barnacle <script> [<optional args>]` to run the Barnacle interpreter on the specified Barnacle script.

Positional arguments:
- `<script>`: The file to interpret. If `-` is provided, read from standard input instead of a file.

Optional arguments:
- `-l <level>` or `--log-level <level>`: Set the interpreter [logging level](https://docs.python.org/3/library/logging.html#logging-levels) (default is `INFO`).
- `--log-file <file>`: Redirect logs to the specified file instead of standard error.
- `--show-tokens`: Output the tokenized stream for the provided script.
- `--show-ast`: Output the Abstract Syntax Tree (AST) for the provided script.
- `--no-run`: Do not interpret the script (useful when combined with `--show-tokens` and/or `--show-ast`).

Examples:
- `python barnacle /example/hello_world.bcl`
- `cat /example/hello_world.bcl | python barnacle -`
- `python barnacle -` (type code directly, to execute use `^D`)
- `python barnacle /example/hello_world.bcl --show-ast --no-run`

## Release History

- v0.1.0: Tokenizer experimentation
- v0.2.0: Parser experimentation
- v0.3.0: Interpreter experimentation
- v0.4.0: Command line features
  - v0.4.1: Pylint, Black and isort
- v0.5.0: Pytest unit testing, variables as expressions
- v0.6.0: Scoped variable declarations, variable re-assignment
- v0.7.0: While loops
- v0.8.0: Mathematical expressions and operations, string concatenation and subtraction
- v0.9.0: Comparison operators (<, >, <=, >=, !=, ==)
- v0.10.0: Function declaration and function calling
- v0.11.0: Do-While loops

## Future Development

Note that these are in no particular order.

- Boolean logic (and, or, xor, not)
- Console input
- For loops
- File I/O

## Special Thanks

Thanks to [Dmitry Soshnikov](https://www.youtube.com/c/DmitrySoshnikov-education) for his YouTube videos on parsing!
