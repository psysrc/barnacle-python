"""
Unit tests for the comparison operators of the bcl_parser submodule.
"""

from .parser_helpers import verify_ast

# Lots of duplication in these unit tests simply because a lot of the AST output is very similar.
# pylint: disable=duplicate-code


def test_equality_integer_literals():
    """Handling equality of two integer literals."""

    verify_ast(
        source="let x = 5 == 5",
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
                        "operator": "==",
                        "left": {
                            "type": "numeric_literal",
                            "value": 5,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 5,
                        },
                    },
                }
            ],
        },
    )


def test_equality_two_variables():
    """Handling equality of two variables."""

    verify_ast(
        source="let eq = x == y",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "eq",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "==",
                        "left": {
                            "type": "identifier",
                            "name": "x",
                        },
                        "right": {
                            "type": "identifier",
                            "name": "y",
                        },
                    },
                }
            ],
        },
    )


def test_equality_variable_and_string_literal():
    """Handling equality of a variable and a string literal."""

    verify_ast(
        source='let ok = ret == "200 OK"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "ok",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "==",
                        "left": {
                            "type": "identifier",
                            "name": "ret",
                        },
                        "right": {
                            "type": "string_literal",
                            "value": "200 OK",
                        },
                    },
                }
            ],
        },
    )


def test_inequality_integer_literals():
    """Handling inequality of two integer literals."""

    verify_ast(
        source="let x = 6 != 7",
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
                        "operator": "!=",
                        "left": {
                            "type": "numeric_literal",
                            "value": 6,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 7,
                        },
                    },
                }
            ],
        },
    )


def test_inequality_two_variables():
    """Handling inequality of two variables."""

    verify_ast(
        source="let neq = x != y",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "neq",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "!=",
                        "left": {
                            "type": "identifier",
                            "name": "x",
                        },
                        "right": {
                            "type": "identifier",
                            "name": "y",
                        },
                    },
                }
            ],
        },
    )


def test_inequality_variable_and_string_literal():
    """Handling inequality of a variable and a string literal."""

    verify_ast(
        source='let error = ret != "200 OK"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "error",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "!=",
                        "left": {
                            "type": "identifier",
                            "name": "ret",
                        },
                        "right": {
                            "type": "string_literal",
                            "value": "200 OK",
                        },
                    },
                }
            ],
        },
    )
