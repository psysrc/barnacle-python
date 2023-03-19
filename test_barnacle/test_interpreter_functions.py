"""
Unit tests for function capabilities of the bcl_interpreter submodule.
"""

from .interpreter_helpers import expect_error, validate_stdout


def test_function_declaration(capsys):
    """Handling a function declaration."""

    validate_stdout(
        capsys,
        source="""
        func do_nothing() {

        }
        """,
        expected_stdout="",
    )


def test_function_redeclaration_same_environment_throws_error():
    """Handling a function redeclaration, which is not allowed in the same environment."""

    expect_error(
        source="""
        func do_nothing() {

        }

        func do_nothing() {

        }
        """,
        exception=RuntimeError,
    )


def test_function_redeclaration_different_environment_is_ok(capsys):
    """Handling a function redeclaration, which is allowed between different environments."""

    validate_stdout(
        capsys,
        source="""
        func do_nothing() {

        }

        {
            func do_nothing() {

            }
        }
        """,
        expected_stdout="",
    )


def test_function_call_as_statement(capsys):
    """Handling a function call as a statement."""

    validate_stdout(
        capsys,
        source="""
        func say_hello() {
            print "Hello World!"
        }

        say_hello()
        say_hello()
        """,
        expected_stdout="Hello World!\nHello World!\n",
    )


def test_function_call_as_expression(capsys):
    """Handling a function call as an expression."""

    validate_stdout(
        capsys,
        source="""
        func get_message() {
            return "Hello Return!"
            return "Goodbye..."
        }

        let x = get_message()
        print x
        """,
        expected_stdout="Hello Return!\n",
    )


def test_function_call_as_statement_with_parameters(capsys):
    """Handling a function call as a statement with two parameters."""

    validate_stdout(
        capsys,
        source="""
        func say_hello(first_name, last_name) {
            print "Hello " + first_name + " " + last_name + "!"
        }

        say_hello("Robert", "Alfreddos")
        """,
        expected_stdout="Hello Robert Alfreddos!\n",
    )


def test_function_call_as_statement_returning_value(capsys):
    """Handling a function call as a statement that returns a value (the value can be ignored)."""

    validate_stdout(
        capsys,
        source="""
        func get_magic_number() {
            return 6
        }

        get_magic_number()
        print "OK"
        """,
        expected_stdout="OK\n",
    )


def test_function_call_as_expression_returning_parameter(capsys):
    """Handling a function call as an expression that returns one of its parameters."""

    validate_stdout(
        capsys,
        source="""
        func identity(value) {
            return value
        }

        print identity(6)
        """,
        expected_stdout="6\n",
    )


def test_function_call_as_expression_returning_local_variable(capsys):
    """Handling a function call as an expression that returns the value of a local variable."""

    validate_stdout(
        capsys,
        source="""
        func plus_one(number) {
            return number + 1
        }

        print plus_one(5)
        """,
        expected_stdout="6\n",
    )


def test_function_call_with_embedded_return_statement_in_code_block(capsys):
    """Handling a function call that has a nested return statement within a code block."""

    validate_stdout(
        capsys,
        source="""
        func get_foo() {
            {
                return "foo"
            }

            return "bar"
        }

        print get_foo()
        """,
        expected_stdout="foo\n",
    )


def test_function_call_with_embedded_return_statement_in_if_statement_on_true(capsys):
    """Handling a function call that has a nested return statement within an if-statement's truth block."""

    validate_stdout(
        capsys,
        source="""
        func get_foo() {
            if true {
                return "foo"
            } else {
                return "bar"
            }

            return "baz"
        }

        print get_foo()
        """,
        expected_stdout="foo\n",
    )


def test_function_call_with_embedded_return_statement_in_if_statement_on_else(capsys):
    """Handling a function call that has a nested return statement within an if-statement's else block."""

    validate_stdout(
        capsys,
        source="""
        func get_bar() {
            if false {
                return "foo"
            } else {
                return "bar"
            }

            return "baz"
        }

        print get_bar()
        """,
        expected_stdout="bar\n",
    )


def test_function_call_with_embedded_return_statement_in_while_statement(capsys):
    """Handling a function call that has a nested return statement within a while loop."""

    validate_stdout(
        capsys,
        source="""
        func get_foo() {
            let n = 3
            while n > 0 {
                n = n - 1
                return "foo"
            }

            return "bar"
        }

        print get_foo()
        """,
        expected_stdout="foo\n",
    )


# TODO: Function (as expression) returning a value from an inner code block structure
# TODO: Function not returning any value (as expression, should throw)
# TODO: Function accessing/modifying global variables
# TODO: Function accessing/modifying variables in outer scope (not global)
#       (i.e. inner functions) (do I want to allow this this?)
# TODO: Function with complex parameters (sub-function call, maths expression, etc)
# TODO: Recursive function
