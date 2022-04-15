# barnacle
An experimental interpreted programming language written in Python.

Aptly named because barnacles don't do a lot, are rough around the edges, and will cause you pain if you work with them too much.

A similar GitHub project exists, [barnacle-rust](https://github.com/psysrc/barnacle-rust), which is intended to become an implementation of **barnacle** written in Rust.
The Python implementation of **barnacle** is intended mostly for experimentation.

## Build

Run `pip install .` to build and install the `barnacle` Python module.

## Usage

Run `python barnacle <script> [<optional args>]` to run the Barnacle interpreter on the specified Barnacle script.

Optional arguments:
- `-l <level>` or `--log-level <level>`: Sets the interpreter [logging level](https://docs.python.org/3/library/logging.html#logging-levels) (default is `INFO`)
- `--log-file <file>`: Redirects logs to the specified file instead of standard out

## Future Development Roadmap
- v0.1: Tokenizer experimentation
- v0.2: Parser experimentation
- v0.3: Interpreter experimentation
- v???: ???

## Special Thanks
Thanks to Dmitry Soshnikov for his [YouTube playlist](https://www.youtube.com/playlist?list=PLGNbPb3dQJ_6aPNnlBvXGyNMlDtNTqN5I)
on Parsing Algorithms!
