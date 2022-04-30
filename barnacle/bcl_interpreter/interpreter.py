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
        self.__interpret_program(self.__ast)

    def __validate_node(self, ast: dict, expected_type: str, expected_keys: set):
        """
        Validates that the AST node has the expected type and contains the expected keys.

        An AST node should always have a `type` key, so this does not need to be provided when calling this function.
        """
        expected_keys = expected_keys.union({"type"})

        if "type" in ast.keys() and ast["type"] != expected_type:
            actual_type = ast["type"]
            raise RuntimeError(f"Node has unexpected type (expected '{expected_type}', got '{actual_type}')")

        if set(ast.keys()) != expected_keys:
            raise RuntimeError(f"Node does not contain the expected keys (expected '{expected_keys}', got '{set(ast.keys())}')")

    def __interpret_program(self, ast: dict):
        self.__validate_node(ast, "program", {"body"})

        for statement in ast["body"]:
            self.__interpret_statement(statement)

    def __interpret_statement(self, ast: dict):
        # TODO: Implement this method properly
        self.__interpret_print(ast)

    def __interpret_print(self, ast: dict):
        self.__validate_node(ast, "print", {"body"})

        string = self.__interpret_string_literal(ast["body"])

        print(string)

    def __interpret_string_literal(self, ast: dict) -> str:
        self.__validate_node(ast, "string_literal", {"value"})

        return ast["value"]

    def __interpret_boolean_literal(self, ast: dict) -> bool:
        self.__validate_node(ast, "boolean_literal", {"value"})

        return ast["value"]