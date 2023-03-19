"""
Unit tests for the basic (non-maths) behaviour of the bcl_parser submodule.
"""

from .parser_helpers import verify_ast

# Lots of duplication in these unit tests simply because a lot of the AST output is very similar.
# pylint: disable=duplicate-code


def test_empty():
    """Handling sources which do not contribute to the AST."""

    def __verify_empty_ast(source: str):
        """Verify that the source produces an empty AST when parsed."""
        verify_ast(source, {"type": "program", "body": []})

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


def test_empty_print():
    """Handling a print statement with an empty string literal."""

    verify_ast(
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


def test_print_hello_world():
    """Handling a print statement with a Hello World string literal."""

    verify_ast(
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


def test_print_three_times():
    """Handling three onsecutive print statements with string literals."""

    verify_ast(
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


def test_print_with_variable():
    """Handling a print statement with a string variable."""

    verify_ast(
        source="""
        let str = "Hello World!"
        print str
        """,
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "str",
                    },
                    "value": {
                        "type": "string_literal",
                        "value": "Hello World!",
                    },
                },
                {
                    "type": "print",
                    "body": {
                        "type": "identifier",
                        "name": "str",
                    },
                },
            ],
        },
    )


def test_while_true_print():
    """Handling WHILE statements."""

    verify_ast(
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

    verify_ast(
        source="let y = 5",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "y",
                    },
                    "value": {
                        "type": "numeric_literal",
                        "value": 5,
                    },
                }
            ],
        },
    )


def test_basic_function_declaration_no_params():
    """Handling a basic function declaration that has no parameters."""

    verify_ast(
        source="""
func say_hello() {
    print "Hello!"
}
""",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "say_hello",
                    },
                    "parameters": [],
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "print",
                                "body": {
                                    "type": "string_literal",
                                    "value": "Hello!",
                                },
                            },
                        ],
                    },
                }
            ],
        },
    )


def test_basic_function_declaration_one_param():
    """Handling a basic function declaration that has one parameter."""

    verify_ast(
        source="""
func say_hello(name) {
    let greeting = "Hello " + name
    print greeting
}
""",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "say_hello",
                    },
                    "parameters": [
                        {
                            "type": "identifier",
                            "name": "name",
                        }
                    ],
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "var_declaration",
                                "identifier": {
                                    "type": "identifier",
                                    "name": "greeting",
                                },
                                "value": {
                                    "type": "binary_expression",
                                    "operator": "+",
                                    "left": {
                                        "type": "string_literal",
                                        "value": "Hello ",
                                    },
                                    "right": {
                                        "type": "identifier",
                                        "name": "name",
                                    },
                                },
                            },
                            {
                                "type": "print",
                                "body": {
                                    "type": "identifier",
                                    "name": "greeting",
                                },
                            },
                        ],
                    },
                }
            ],
        },
    )


def test_basic_function_declaration_three_params():
    """Handling a basic function declaration that has three parameters."""

    verify_ast(
        source="""
func three_way_adder(num1, num2, num3) {
    let answer = num1 + num2 + num3
    print answer
}
""",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "three_way_adder",
                    },
                    "parameters": [
                        {
                            "type": "identifier",
                            "name": "num1",
                        },
                        {
                            "type": "identifier",
                            "name": "num2",
                        },
                        {
                            "type": "identifier",
                            "name": "num3",
                        },
                    ],
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "var_declaration",
                                "identifier": {
                                    "type": "identifier",
                                    "name": "answer",
                                },
                                "value": {
                                    "type": "binary_expression",
                                    "operator": "+",
                                    "left": {
                                        "type": "binary_expression",
                                        "operator": "+",
                                        "left": {
                                            "type": "identifier",
                                            "name": "num1",
                                        },
                                        "right": {
                                            "type": "identifier",
                                            "name": "num2",
                                        },
                                    },
                                    "right": {
                                        "type": "identifier",
                                        "name": "num3",
                                    },
                                },
                            },
                            {
                                "type": "print",
                                "body": {
                                    "type": "identifier",
                                    "name": "answer",
                                },
                            },
                        ],
                    },
                }
            ],
        },
    )


def test_basic_function_declaration_one_param_return_param():
    """Handling a basic function declaration that has one parameter which is returned."""

    verify_ast(
        source="""
func do_nothing(value) {
    return value
}
""",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "do_nothing",
                    },
                    "parameters": [
                        {
                            "type": "identifier",
                            "name": "value",
                        }
                    ],
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "return",
                                "body": {
                                    "type": "identifier",
                                    "name": "value",
                                },
                            },
                        ],
                    },
                }
            ],
        },
    )


def test_basic_function_declaration_return_literal():
    """Handling a basic function declaration which returns a literal value."""

    verify_ast(
        source="""
func get_foo() {
    return "foo"
}
""",
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "get_foo",
                    },
                    "parameters": [],
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "return",
                                "body": {
                                    "type": "string_literal",
                                    "value": "foo",
                                },
                            },
                        ],
                    },
                }
            ],
        },
    )


def test_basic_function_call_as_statement():
    """Handling a basic function call via a standalone statement."""

    verify_ast(
        source="""
        func do_nothing() {

        }

        do_nothing()
        """,
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "do_nothing",
                    },
                    "parameters": [],
                    "body": {
                        "type": "code_block",
                        "body": [],
                    },
                },
                {
                    "type": "func_call",
                    "identifier": {
                        "type": "identifier",
                        "name": "do_nothing",
                    },
                    "parameters": [],
                },
            ],
        },
    )


def test_complex_function_call_as_statement():
    """Handling a complex function call (many params) via a standalone statement."""

    verify_ast(
        source="""
        func do_nothing(param1, param2, param3) {

        }

        do_nothing("hi", 4, -0.2)
        """,
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "do_nothing",
                    },
                    "parameters": [
                        {
                            "type": "identifier",
                            "name": "param1",
                        },
                        {
                            "type": "identifier",
                            "name": "param2",
                        },
                        {
                            "type": "identifier",
                            "name": "param3",
                        },
                    ],
                    "body": {
                        "type": "code_block",
                        "body": [],
                    },
                },
                {
                    "type": "func_call",
                    "identifier": {
                        "type": "identifier",
                        "name": "do_nothing",
                    },
                    "parameters": [
                        {
                            "type": "string_literal",
                            "value": "hi",
                        },
                        {
                            "type": "numeric_literal",
                            "value": 4,
                        },
                        {
                            "type": "numeric_literal",
                            "value": -0.2,
                        },
                    ],
                },
            ],
        },
    )


def test_basic_function_call_as_expression():
    """Handling a basic function call via an expression."""

    verify_ast(
        source="""
        func empty_string() {
            return ""
        }

        let e = empty_string()
        """,
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "empty_string",
                    },
                    "parameters": [],
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "return",
                                "body": {
                                    "type": "string_literal",
                                    "value": "",
                                },
                            },
                        ],
                    },
                },
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "e",
                    },
                    "value": {
                        "type": "func_call",
                        "identifier": {
                            "type": "identifier",
                            "name": "empty_string",
                        },
                        "parameters": [],
                    }
                },
            ],
        },
    )


def test_complex_function_call_as_expression():
    """Handling a complex function call (many params) via an expression."""

    verify_ast(
        source="""
        func empty_string(param1, param2, param3) {
            return ""
        }

        let e = empty_string(1, -6, "soul")
        """,
        expected_ast={
            "type": "program",
            "body": [
                {
                    "type": "func_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "empty_string",
                    },
                    "parameters": [
                        {
                            "type": "identifier",
                            "name": "param1",
                        },
                        {
                            "type": "identifier",
                            "name": "param2",
                        },
                        {
                            "type": "identifier",
                            "name": "param3",
                        },
                    ],
                    "body": {
                        "type": "code_block",
                        "body": [
                            {
                                "type": "return",
                                "body": {
                                    "type": "string_literal",
                                    "value": "",
                                },
                            },
                        ],
                    },
                },
                {
                    "type": "var_declaration",
                    "identifier": {
                        "type": "identifier",
                        "name": "e",
                    },
                    "value": {
                        "type": "func_call",
                        "identifier": {
                            "type": "identifier",
                            "name": "empty_string",
                        },
                        "parameters": [
                            {
                                "type": "numeric_literal",
                                "value": 1,
                            },
                            {
                                "type": "numeric_literal",
                                "value": -6,
                            },
                            {
                                "type": "string_literal",
                                "value": "soul",
                            },
                        ],
                    }
                },
            ],
        },
    )
