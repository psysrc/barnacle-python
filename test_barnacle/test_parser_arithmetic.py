"""
Unit tests for the arithmetic operators of the bcl_parser submodule.
"""

from .parser_helpers import verify_ast

# Lots of duplication in these unit tests simply because a lot of the AST output is very similar.
# pylint: disable=duplicate-code


def test_add_two_integer_literals():
    """Handling addition of two integer literals."""

    verify_ast(
        source="let x = 5 + 5",
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


def test_add_two_float_literals():
    """Handling addition of two float literals."""

    verify_ast(
        source="let x = 1.2 + 2.1",
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
                            "type": "numeric_literal",
                            "value": 1.2,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2.1,
                        },
                    },
                }
            ],
        },
    )


def test_add_three_integer_literals():
    """Handling addition of three integer literals."""

    verify_ast(
        source="let x = 1 + 2 + 3",
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
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
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


def test_subtraction_two_integer_literals():
    """Handling subtraction of two integer literals."""

    verify_ast(
        source="let x = 5 - 5",
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


def test_subtraction_two_float_literals():
    """Handling subtraction of two float literals."""

    verify_ast(
        source="let x = 2.1 - 1.2",
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
                            "type": "numeric_literal",
                            "value": 2.1,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 1.2,
                        },
                    },
                }
            ],
        },
    )


def test_addition_and_subtraction_is_left_associative_integer_literals():
    """Handling addition and subtraction of three integer literals, ensuring they are both left-associative."""

    verify_ast(
        source="let x = 1 + 2 - 3",
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
                            "type": "binary_expression",
                            "operator": "+",
                            "left": {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
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

    verify_ast(
        source="let x = 1 - 2 + 3",
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
                            "operator": "-",
                            "left": {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
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


def test_multiplication_two_integer_literals():
    """Handling multiplication of two integer literals."""

    verify_ast(
        source="let x = 2 * 2",
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
                        "operator": "*",
                        "left": {
                            "type": "numeric_literal",
                            "value": 2,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2,
                        },
                    },
                }
            ],
        },
    )


def test_multiplication_two_float_literals():
    """Handling multiplication of two float literals."""

    verify_ast(
        source="let x = 2.5 * 2.5",
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
                        "operator": "*",
                        "left": {
                            "type": "numeric_literal",
                            "value": 2.5,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2.5,
                        },
                    },
                }
            ],
        },
    )


def test_multiplication_integer_and_float_literals():
    """Handling multiplication of an integer literal and a float literal."""

    verify_ast(
        source="let x = 2 * 2.5",
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
                        "operator": "*",
                        "left": {
                            "type": "numeric_literal",
                            "value": 2,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2.5,
                        },
                    },
                }
            ],
        },
    )


def test_division_two_integer_literals():
    """Handling division of two integer literals."""

    verify_ast(
        source="let x = 2 / 2",
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
                        "operator": "/",
                        "left": {
                            "type": "numeric_literal",
                            "value": 2,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2,
                        },
                    },
                }
            ],
        },
    )


def test_division_two_float_literals():
    """Handling division of two float literals."""

    verify_ast(
        source="let x = 2.5 / 2.5",
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
                        "operator": "/",
                        "left": {
                            "type": "numeric_literal",
                            "value": 2.5,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2.5,
                        },
                    },
                }
            ],
        },
    )


def test_division_integer_and_float_literals():
    """Handling division of an integer literal and a float literal."""

    verify_ast(
        source="let x = 2.5 / 2",
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
                        "operator": "/",
                        "left": {
                            "type": "numeric_literal",
                            "value": 2.5,
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2,
                        },
                    },
                }
            ],
        },
    )


def test_multiplication_and_division_is_left_associative_integer_literals():
    """Handling multiplication and division of three integer literals, ensuring they are both left-associative."""

    verify_ast(
        source="let x = 1 * 2 / 3",
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
                        "operator": "/",
                        "left": {
                            "type": "binary_expression",
                            "operator": "*",
                            "left": {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
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

    verify_ast(
        source="let x = 1 / 2 * 3",
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
                        "operator": "*",
                        "left": {
                            "type": "binary_expression",
                            "operator": "/",
                            "left": {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
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


def test_multiplication_has_higher_precedence_than_addition():
    """Handling expressions with both multiplication and addition, ensuring the multiplication takes precedence."""

    verify_ast(
        source="let x = 1 * 2 + 3",
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
                            "operator": "*",
                            "left": {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
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

    verify_ast(
        source="let x = 1 + 2 * 3",
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
                            "type": "numeric_literal",
                            "value": 1,
                        },
                        "right": {
                            "type": "binary_expression",
                            "operator": "*",
                            "left": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 3,
                            },
                        },
                    },
                }
            ],
        },
    )


def test_division_has_higher_precedence_than_subtraction():
    """Handling expressions with both division and subtraction, ensuring the division takes precedence."""

    verify_ast(
        source="let x = 1 / 2 - 3",
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
                            "type": "binary_expression",
                            "operator": "/",
                            "left": {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
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

    verify_ast(
        source="let x = 1 - 2 / 3",
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
                            "type": "numeric_literal",
                            "value": 1,
                        },
                        "right": {
                            "type": "binary_expression",
                            "operator": "/",
                            "left": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 3,
                            },
                        },
                    },
                }
            ],
        },
    )


def test_parentheses_have_precedence_over_everything():
    """Handling expressions with parentheses, ensuring the expression in the parentheses takes precedence."""

    verify_ast(
        source="let x = 1 / (2 - 3)",
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
                        "operator": "/",
                        "left": {
                            "type": "numeric_literal",
                            "value": 1,
                        },
                        "right": {
                            "type": "binary_expression",
                            "operator": "-",
                            "left": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 3,
                            },
                        },
                    },
                },
            ],
        },
    )

    verify_ast(
        source="let x = (1 / 2) - 3",
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
                            "type": "binary_expression",
                            "operator": "/",
                            "left": {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            "right": {
                                "type": "numeric_literal",
                                "value": 2,
                            },
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 3,
                        },
                    },
                },
            ],
        },
    )


def test_nested_parenthesised_expressions():
    """Handling parenthesised expressions inside of parenthesised expressions."""

    verify_ast(
        source="let x = (3 - (1 / 2)) * 4",
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
                        "operator": "*",
                        "left": {
                            "type": "binary_expression",
                            "operator": "-",
                            "left": {
                                "type": "numeric_literal",
                                "value": 3,
                            },
                            "right": {
                                "type": "binary_expression",
                                "operator": "/",
                                "left": {
                                    "type": "numeric_literal",
                                    "value": 1,
                                },
                                "right": {
                                    "type": "numeric_literal",
                                    "value": 2,
                                },
                            },
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 4,
                        },
                    },
                },
            ],
        },
    )


def test_add_integer_to_variable():
    """Handling integer addition involving a variable."""

    verify_ast(
        source="let x = 2 + z",
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
                            "type": "numeric_literal",
                            "value": 2,
                        },
                        "right": {
                            "type": "identifier",
                            "name": "z",
                        },
                    },
                }
            ],
        },
    )

    verify_ast(
        source="let x = z + 2",
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
                            "name": "z",
                        },
                        "right": {
                            "type": "numeric_literal",
                            "value": 2,
                        },
                    },
                }
            ],
        },
    )


def test_addition_two_variables():
    """Handling addition of two variables of indeterminate type."""

    verify_ast(
        source="let x = z + y",
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
                            "name": "z",
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


def test_multiplication_two_variables():
    """Handling multiplication of two variables of indeterminate type."""

    verify_ast(
        source="let x = z * y",
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
                        "operator": "*",
                        "left": {
                            "type": "identifier",
                            "name": "z",
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
