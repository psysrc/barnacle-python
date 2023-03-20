"""
The entry point for the Barnacle command line interpreter.
"""

import argparse
import json
import logging
import sys

from bcl_interpreter import interpreter as itp
from bcl_parser import parser as prs
from bcl_tokenizer import tokenizer as tkn


def get_source_from_stdin() -> str:
    """Read the script source from standard input."""

    logging.info("🐚 Reading Script from STDIN 🐚")

    source = sys.stdin.read()

    return source


def get_source_from_file(script: str) -> str:
    """Read the script source from the specified file."""

    logging.info("🐚 Reading Script '%s' 🐚", script)

    with open(script, "r", encoding="utf-8") as script_file:
        source = script_file.read()

    return source


def output_tokens(source: str):
    """Output the tokenization of the source."""

    logging.info("🐚 Tokenizer Start 🐚")

    tokenizer = tkn.Tokenizer(source)

    while not tokenizer.end_of_stream():
        print(tokenizer.next_token())

    logging.info("🐚 Tokenizer End 🐚")


def output_ast(source: str):
    """Output the AST of the source."""

    logging.info("🐚 Parser Start 🐚")

    parser = prs.Parser(source)
    ast = parser.parse()
    print(json.dumps(ast, indent=4))

    logging.info("🐚 Parser End 🐚")


def interpret_file(source: str):
    """Interpret the source."""

    logging.info("🐚 Interpreter Start 🐚")

    interpreter = itp.Interpreter(source)
    interpreter.run()

    logging.info("🐚 Interpreter End 🐚")


def main():
    """Main entry point to the Barnacle interpreter"""

    cmd_desc = "Barnacle Interpreter"
    arg_parser = argparse.ArgumentParser(description=cmd_desc)

    arg_parser.add_argument("script", help="Barnacle script to interpret (if '-', read from stdin)")
    arg_parser.add_argument("-l", "--log-level", help="Logging level (default INFO)", default="INFO")
    arg_parser.add_argument("--log-file", help="Redirect logs to the provided file instead of standard error")
    arg_parser.add_argument("--show-tokens", help="Output the tokenization of the script", action="store_true")
    arg_parser.add_argument("--show-ast", help="Output the parsed AST of the script", action="store_true")
    arg_parser.add_argument("--no-run", help="Do not interpret the script", action="store_true")

    args = arg_parser.parse_args()

    logging.basicConfig(format="%(asctime)s|%(message)s", filename=args.log_file, level=args.log_level)

    source = get_source_from_stdin() if args.script == "-" else get_source_from_file(args.script)

    if args.show_tokens:
        output_tokens(source)

    if args.show_ast:
        output_ast(source)

    if not args.no_run:
        interpret_file(source)


if __name__ == "__main__":
    main()
