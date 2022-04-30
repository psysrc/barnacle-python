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

    def __validate_node_has_type(self, ast: dict):
        """
        Validates that the AST node has a `type` key.
        """

        if "type" not in ast.keys():
            logging.debug(f"Node has no 'type' key: {ast}")
            raise RuntimeError("Node has no 'type' key")

    def __validate_node(self, ast: dict, expected_type: str, expected_keys: set):
        """
        Validates that the AST node has the expected type and contains the expected keys.

        An AST node should always have a `type` key, so this does not need to be provided when calling this function.
        """

        self.__validate_node_has_type(ast)

        expected_keys = expected_keys.union({"type"})

        if ast["type"] != expected_type:
            actual_type = ast["type"]
            logging.debug(f"Node has unexpected type: {ast}")
            raise RuntimeError(f"Node has unexpected type (expected '{expected_type}', got '{actual_type}')")

        if set(ast.keys()) != expected_keys:
            logging.debug(f"Node does not contain the expected keys: {ast}")
            raise RuntimeError(f"Node does not contain the expected keys (expected '{expected_keys}', got '{set(ast.keys())}')")

    def __interpret_program(self, ast: dict):
        logging.debug("Interpreting 'program' node")
        self.__validate_node(ast, "program", {"body"})

        for statement in ast["body"]:
            self.__interpret_statement(statement)

    def __interpret_statement(self, ast: dict):
        logging.debug("Interpreting 'statement' node")

        branches = {
            "print": self.__interpret_print,
            "conditional": self.__interpret_conditional,
        }

        self.__construct_multibranch_interpret(ast, "statement", branches)

    def __interpret_print(self, ast: dict):
        logging.debug("Interpreting 'print' node")
        self.__validate_node(ast, "print", {"body"})

        string = self.__interpret_string_literal(ast["body"])

        print(string)

    def __interpret_string_literal(self, ast: dict):
        logging.debug("Interpreting 'string_literal' node")
        self.__validate_node(ast, "string_literal", {"value"})

        return ast["value"]

    def __interpret_numeric_literal(self, ast: dict):
        logging.debug("Interpreting 'numeric_literal' node")
        self.__validate_node(ast, "numeric_literal", {"value"})

        return ast["value"]

    def __interpret_boolean_literal(self, ast: dict):
        logging.debug("Interpreting 'boolean_literal' node")
        self.__validate_node(ast, "boolean_literal", {"value"})

        return ast["value"]

    def __interpret_expression(self, ast: dict):
        logging.debug("Interpreting 'expression' node")

        branches = {
            "string_literal": self.__interpret_string_literal,
            "numeric_literal": self.__interpret_numeric_literal,
            "boolean_literal": self.__interpret_boolean_literal,
        }

        return self.__construct_multibranch_interpret(ast, "expression", branches)

    def __construct_multibranch_interpret(self, ast, interpret_name, branches):
        self.__validate_node_has_type(ast)

        node_type = ast["type"]

        if node_type in branches:
            return branches[node_type](ast)

        logging.debug(f"Unexpected node type while interpreting '{interpret_name}' node: {ast}")
        raise RuntimeError(f"Unexpected node type '{node_type}' while interpreting '{interpret_name}'")

    def __interpret_conditional(self, ast: dict):
        logging.debug("Interpreting 'conditional' node")
        self.__validate_node(ast, "conditional", {"expression", "on_true", "on_false"})

        expression = self.__interpret_expression(ast["expression"])

        if bool(expression):
            logging.debug("Interpreting conditional 'on_true' node")
            self.__interpret_code_block(ast["on_true"])
        elif (on_false_ast := ast["on_false"]) is not None:
            logging.debug("Interpreting conditional 'on_false' node")
            self.__validate_node_has_type(on_false_ast)

            if on_false_ast["type"] == "conditional":
                self.__interpret_conditional(on_false_ast)
            else:
                self.__interpret_code_block(on_false_ast)

    def __interpret_code_block(self, ast: dict):
        logging.debug("Interpreting 'code_block' node")
        self.__validate_node(ast, "code_block", {"body"})

        for statement in ast["body"]:
            self.__interpret_statement(statement)
