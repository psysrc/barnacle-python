"""
interpreter.py: Implements the Interpreter class.
"""

import logging
import json

from bcl_parser import parser as prs


class Interpreter:
    """
    The Barnacle Interpreter.
    """

    def __init__(self):
        pass

    @staticmethod
    def run(filename: str):
        """Runs the Barnacle interpreter on the specified file."""

        logging.debug(f"Opening file '{filename}'")

        with open(filename, "r") as script:
            source = script.read()

        logging.info(f"Running script '{filename}'")
        print(f"+++ BARNACLE RUN '{filename}' +++")

        parser = prs.Parser(source)
        print(json.dumps(parser.parse(), indent=4))

        print(f"--- BARNACLE END '{filename}' ---")
        logging.info(f"Finished interpreting script")
