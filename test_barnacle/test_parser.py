"""
test_parser.py: Unit tests for the bcl_parser submodule.
"""

from bcl_parser import parser as prs


def __verify_ast(source: str, expected_ast: dict):
    """Verify that the source produces the expected AST when parsed."""

    parser = prs.Parser(source)

    actual_ast = parser.parse()

    assert actual_ast == expected_ast


def test_empty():
    """Handling an empty source string."""

    source = ""

    expected_ast = {
        "type": "program",
        "body": [],
    }

    __verify_ast(source, expected_ast)
