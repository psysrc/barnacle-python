"""
test_parser.py: Unit tests for the bcl_parser submodule.
"""

from bcl_parser import parser as prs


def test_empty():
    """Handling an empty source string."""

    parser = prs.Parser("")

    expected_ast = {
        "type": "program",
        "body": [],
    }

    actual_ast = parser.parse()

    assert actual_ast == expected_ast
