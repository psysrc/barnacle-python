"""
main.py: The entry point for the Barnacle command line interpreter.
"""

import logging
import argparse
from bcl_interpreter import interpreter as itp


def interpret_file(script: str):
    logging.debug(f"Opening file '{script}'")

    with open(script, "r") as script:
        source = script.read()

    logging.info(f"🐚 BARNACLE START '{script}' 🐚")

    interpreter = itp.Interpreter(source)
    interpreter.run()

    logging.info(f"🐚 BARNACLE END '{script}' 🐚")


def main():
    """Main entry point to the Barnacle interpreter"""

    cmd_desc = "Barnacle Interpreter"
    arg_parser = argparse.ArgumentParser(description=cmd_desc)

    arg_parser.add_argument("script", help="Barnacle script to execute")
    arg_parser.add_argument("-l", "--log-level", help="Logging level", default="INFO")
    arg_parser.add_argument("--log-file", help="File to write interpreter logs to")

    args = arg_parser.parse_args()

    logging.basicConfig(format="%(asctime)s|%(message)s", filename=args.log_file, level=args.log_level)

    interpret_file(args.script)



if __name__ == "__main__":
    main()
