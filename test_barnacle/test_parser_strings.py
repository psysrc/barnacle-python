"""
Unit tests for string handling of the bcl_parser submodule.
"""

from .parser_helpers import verify_ast

# Lots of duplication in these unit tests simply because a lot of the AST output is very similar.
# pylint: disable=duplicate-code


def test_variable_assignment_string_literal():
    """Handling a variable declaration with a single string literal."""

    verify_ast(
        source='let x = "Hello World"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "x",
                    },
                    "value": {
                        "type": "string_literal",
                        "value": "Hello World",
                    },
                }
            ],
        },
    )


def test_add_two_string_literals():
    """Handling addition of two string literals."""

    verify_ast(
        source='let x = "Hello" + " World"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "x",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "+",
                        "left": {
                            "type": "string_literal",
                            "value": "Hello",
                        },
                        "right": {
                            "type": "string_literal",
                            "value": " World",
                        },
                    },
                }
            ],
        },
    )


def test_add_three_string_literals():
    """Handling addition of three string literals."""

    verify_ast(
        source='let x = "Hello" + " " + "World"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "x",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "+",
                        "left": {
                            "type": "binary_expression",
                            "operator": "+",
                            "left": {
                                "type": "string_literal",
                                "value": "Hello",
                            },
                            "right": {
                                "type": "string_literal",
                                "value": " ",
                            },
                        },
                        "right": {
                            "type": "string_literal",
                            "value": "World",
                        },
                    },
                }
            ],
        },
    )


def test_subtract_two_string_literals():
    """Handling subtraction of two string literals."""

    verify_ast(
        source='let x = "Hello World" - " World"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "x",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "-",
                        "left": {
                            "type": "string_literal",
                            "value": "Hello World",
                        },
                        "right": {
                            "type": "string_literal",
                            "value": " World",
                        },
                    },
                }
            ],
        },
    )


def test_string_addition_to_variable():
    """Handling addition of a string literal to a variable."""

    verify_ast(
        source='let x = first_name + " Halibut"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "x",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "+",
                        "left": {
                            "type": "identifier",
                            "name": "first_name",
                        },
                        "right": {
                            "type": "string_literal",
                            "value": " Halibut",
                        },
                    },
                }
            ],
        },
    )
