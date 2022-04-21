"""
interpreter.py: Implements the Interpreter class.
"""

import logging

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
        parser.parse()

        print(f"--- BARNACLE END '{filename}' ---")
        logging.info(f"Finished interpreting script")
