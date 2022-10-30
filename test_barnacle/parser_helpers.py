"""
parser_helpers.py: Implements helper functions for the bcl_parser unit tests.
"""

from bcl_parser import parser as prs


def verify_ast(source: str, expected_ast: dict):
    """Verify that the source produces the expected AST when parsed."""

    parser = prs.Parser(source)

    actual_ast = parser.parse()

    assert actual_ast == expected_ast
