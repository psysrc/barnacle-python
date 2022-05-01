"""
main.py: The entry point for the Barnacle command line interpreter.
"""

import logging
import argparse
import json
import sys
from bcl_tokenizer import tokenizer as tkn
from bcl_parser import parser as prs
from bcl_interpreter import interpreter as itp


def get_source_from_stdin() -> str:
    logging.info("🐚 Reading Script from STDIN 🐚")

    source = sys.stdin.read()

    return source


def get_source_from_file(script: str) -> str:
    logging.info(f"🐚 Reading Script '{script}' 🐚")

    with open(script, "r") as script_file:
        source = script_file.read()

    return source


def output_tokens(source: str):
    logging.info("🐚 Tokenizer Start 🐚")

    tokenizer = tkn.Tokenizer(source)

    while (token := tokenizer.next_token()):
        print(token)

    logging.info("🐚 Tokenizer End 🐚")


def output_ast(source: str):
    logging.info("🐚 Parser Start 🐚")

    parser = prs.Parser(source)
    ast = parser.parse()
    print(json.dumps(ast, indent=4))

    logging.info("🐚 Parser End 🐚")


def interpret_file(source: str):
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
    arg_parser.add_argument("--log-file", help="Optional file to write logs to")
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
