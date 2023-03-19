"""
Unit tests for function capabilities of the bcl_interpreter submodule.
"""

from bcl_interpreter import interpreter as itp

from .interpreter_helpers import expect_error, validate_stdout


def test_function_declaration(capsys):
    """Handling a basic function declaration."""

    validate_stdout(
        capsys,
        source="""
        func do_nothing() {

        }
        """,
        expected_stdout="",
    )


def test_function_redeclaration_same_environment_throws_error():
    """Handling a basic function redeclaration, which is not allowed in the same environment."""

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
    """Handling a basic function redeclaration, which is allowed between different environments."""

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


def test_basic_function_call_as_statement(capsys):
    """Handling a basic function call as a statement."""

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


def test_basic_function_call_as_expression(capsys):
    """Handling a basic function call as an expression."""

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


# TODO: Function with parameters
# TODO: Function returning a value (as statement)
# TODO: Function (as expression) returning a value from an inner code block structure
# TODO: Function not returning any value (as expression, should throw)
# TODO: Function returning a parameter
# TODO: Function returning a local variable
# TODO: Function accessing/modifying global variables
# TODO: Function accessing/modifying variables in outer scope (not global)
#       (i.e. inner functions) (do I want to allow this this?)
# TODO: Function with complex parameters (sub-function call, maths expression, etc)
