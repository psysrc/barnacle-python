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


def test_less_than_two_variables():
    """Handling the less-than operator between two variables."""

    verify_ast(
        source="let less = x < y",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "less",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "<",
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


def test_less_than_variable_and_integer_literal():
    """Handling the less-than operator between a variable and an integer literal."""

    verify_ast(
        source='let v = ret < 3',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "v",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "<",
                        "left": {
                            "type": "identifier",
                            "name": "ret",
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 3,
                        },
                    },
                }
            ],
        },
    )


def test_less_than_or_equal_two_variables():
    """Handling the less-than-or-equal operator between two variables."""

    verify_ast(
        source="let less_or_eq = x <= y",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "less_or_eq",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "<=",
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


def test_less_than_or_equal_variable_and_integer_literal():
    """Handling the less-than-or-equal operator between a variable and an integer literal."""

    verify_ast(
        source='let v = ret <= 3',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "v",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": "<=",
                        "left": {
                            "type": "identifier",
                            "name": "ret",
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 3,
                        },
                    },
                }
            ],
        },
    )


def test_more_than_two_variables():
    """Handling the more-than operator between two variables."""

    verify_ast(
        source="let more = x > y",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "more",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": ">",
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


def test_more_than_variable_and_integer_literal():
    """Handling the more-than operator between a variable and an integer literal."""

    verify_ast(
        source='let v = ret > 3',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "v",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": ">",
                        "left": {
                            "type": "identifier",
                            "name": "ret",
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 3,
                        },
                    },
                }
            ],
        },
    )


def test_more_than_or_equal_two_variables():
    """Handling the more-than-or-equal operator between two variables."""

    verify_ast(
        source="let more_or_eq = x >= y",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "more_or_eq",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": ">=",
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


def test_more_than_or_equal_variable_and_integer_literal():
    """Handling the more-than-or-equal operator between a variable and an integer literal."""

    verify_ast(
        source='let v = ret >= 3',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "v",
                    },
                    "value": {
                        "type": "binary_expression",
                        "operator": ">=",
                        "left": {
                            "type": "identifier",
                            "name": "ret",
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 3,
                        },
                    },
                }
            ],
        },
    )
