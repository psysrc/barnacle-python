import logging
import argparse
from interpreter import interpreter


def main():
    """Main entry point to the Barnacle interpreter"""

    cmd_desc = "Barnacle Interpreter"
    arg_parser = argparse.ArgumentParser(description=cmd_desc)

    arg_parser.add_argument("script", help="Barnacle script to execute")
    arg_parser.add_argument("-l", "--log-level", help="Logging level", default="INFO")
    arg_parser.add_argument("--log-file", help="File to write interpreter logs to")

    args = arg_parser.parse_args()

    logging.basicConfig(format="%(asctime)s|%(message)s", filename=args.log_file, level=args.log_level)

    interpreter.run(args.script)



if __name__ == "__main__":
    main()
