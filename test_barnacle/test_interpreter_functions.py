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


def test_function_call_with_embedded_return_statement_in_do_while_statement(capsys):
    """Handling a function call that has a nested return statement within a do-while loop."""

    validate_stdout(
        capsys,
        source="""
        func get_foo() {
            let n = 3
            do {
                n = n - 1
                return "foo"
            } while n > 0

            return "bar"
        }

        print get_foo()
        """,
        expected_stdout="foo\n",
    )


def test_function_call_as_expression_without_returning_any_value():
    """Handling a function call as an expression, when a return value is not provided during function execution."""

    expect_error(
        source="""
        func no_return() {

        }

        let s = no_return()
        """,
        exception=RuntimeError,
    )


def test_function_call_recursively_calling_itself(capsys):
    """Handling a function call that recursively calls itself."""

    validate_stdout(
        capsys,
        source="""
        func fibonacci(number) {
            if number == 0 {
                return 0
            }

            if number == 1 {
                return 1
            }

            return fibonacci(number - 1) + fibonacci(number - 2)
        }

        print fibonacci(7)
        """,
        expected_stdout="13\n",
    )


def test_complex_function_call(capsys):
    """Handling a function call that involves resolving several parameters of complex expressions."""

    validate_stdout(
        capsys,
        source="""
        func plus_one(number) {
            return number + 1
        }

        func print_times(message, times) {
            while times > 0 {
                print message
                times = times - 1
            }
        }

        print_times("LWR" - ("W" + "R"), plus_one(1 + plus_one(3 - 2)) - (-2 + 4))
        """,
        expected_stdout="L\nL\n",
    )


def test_function_call_accessing_global_variables(capsys):
    """Handling a function call that accesses global variables."""

    validate_stdout(
        capsys,
        source="""
        let g = "Global"

        func print_g() {
            print g
        }

        print_g()
        """,
        expected_stdout="Global\n",
    )


def test_function_call_modifying_global_variables(capsys):
    """Handling a function call that modifies global variables."""

    validate_stdout(
        capsys,
        source="""
        let g = "Global"

        func change_g() {
            g = "GLOBAL"
        }

        change_g()
        print g
        """,
        expected_stdout="GLOBAL\n",
    )


def test_function_call_accessing_outer_scope_variables(capsys):
    """Handling a function call that accesses variables in an outer (non-global) scope."""

    validate_stdout(
        capsys,
        source="""
        func outer() {
            let o = "Outer"

            func inner() {
                print o
            }

            inner()
        }

        outer()
        """,
        expected_stdout="Outer\n",
    )


def test_function_call_modifying_outer_scope_variables(capsys):
    """Handling a function call that modifies variables in an outer (non-global) scope."""

    validate_stdout(
        capsys,
        source="""
        func outer() {
            let o = "Outer"

            func inner() {
                o = "Inner"
            }

            inner()
            print o
        }

        outer()
        """,
        expected_stdout="Inner\n",
    )
