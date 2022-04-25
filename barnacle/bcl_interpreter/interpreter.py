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

    def __init__(self, source: str):
        self.__ast = prs.Parser(source).parse()
        logging.debug("Finished parsing source")

    def run(self):
        """Runs the Barnacle interpreter on the provided source."""
        print(json.dumps(self.__ast, indent=4))
