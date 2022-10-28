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
    """Handling sources which do not contribute to the AST."""

    def __verify_empty_ast(source: str):
        """Verify that the source produces an empty AST when parsed."""
        __verify_ast(source, {"type": "program", "body": []})

    __verify_empty_ast("")

    __verify_empty_ast("     \n  \n\n\n \t  \n \r\n \t\t\t\r\n\r\n   \t\n")

    __verify_empty_ast("/* Just a block comment! */")

    __verify_empty_ast("// Just a single line comment!")

    __verify_empty_ast(
        """\
/* Just lots of comments and whitespace */
\n\n\n\n\n \t\t\t\t \r\n\r\n\r\n
// COMMENT        COMMENT       COMMENT
/* Multi
    Line
    Comment
*/
"""
    )


def test_print():
    """Handling print statements."""

    __verify_ast(
        source='print ""',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "print",
                    "body": {
                        "type": "string_literal",
                        "value": "",
                    },
                },
            ],
        },
    )
    __verify_ast(
        source='print "Hello World!"',
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "print",
                    "body": {
                        "type": "string_literal",
                        "value": "Hello World!",
                    },
                },
            ],
        },
    )

    __verify_ast(
        source="""
print "Hello World!"
print "Second line!"
print "Third line!!"
""",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "print",
                    "body": {
                        "type": "string_literal",
                        "value": "Hello World!",
                    },
                },
                {
                    "type": "print",
                    "body": {
                        "type": "string_literal",
                        "value": "Second line!",
                    },
                },
                {
                    "type": "print",
                    "body": {
                        "type": "string_literal",
                        "value": "Third line!!",
                    },
                },
            ],
        },
    )


def test_while_true_print():
    """Handling WHILE statements."""

    __verify_ast(
        source="""
while true {
    print "While True Do"
}
""",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "while",
                    "expression": {
                        "type": "boolean_literal",
                        "value": True,
                    },
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "print",
                                "body": {
                                    "type": "string_literal",
                                    "value": "While True Do",
                                },
                            },
                        ],
                    },
                },
            ],
        },
    )


def test_basic_variable_declaration():
    """Handling basic variable declarations."""

    __verify_ast(
        source="let x = 5",
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
                        "type": "numeric_literal",
                        "value": 5,
                    },
                }
            ],
        },
    )


def test_additive_expressions():
    """Handling additive expressions."""

    __verify_ast(
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

    __verify_ast(
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

    __verify_ast(
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
