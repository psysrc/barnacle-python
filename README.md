# barnacle
An experimental interpreted programming language written in Python.

Aptly named because barnacles don't do a lot, are rough around the edges, and will cause you pain if you work with them too much.

## Build

1. Create a Python3 virtual environment with `python3 -m venv <venv name>`.
2. Activate the newly created virtual environment with `source <venv name>/bin/activate`.
3. Update pip with `pip install -U pip`.
4. Install dependencies with `pip install -U -r requirements.txt`.
5. Run `pip install .` to build and install the `barnacle` Python module.

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
- `python barnacle examples/hello_world.bcl`
- `cat examples/hello_world.bcl | python barnacle -`
- `python barnacle -` (type code on the fly, to finish use `^D`)
- `python barnacle examples/basic_program.bcl --show-ast --no-run`

## Release History
- v0.1: Tokenizer experimentation
- v0.2: Parser experimentation
- v0.3: Interpreter experimentation

## Future Development Roadmap
- v0.4: Command line features
- v0.5: Unit testing
- v0.6: ???

## Special Thanks
Thanks to [Dmitry Soshnikov](https://www.youtube.com/c/DmitrySoshnikov-education) for his YouTube videos on parsing!
