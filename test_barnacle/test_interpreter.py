"""
test_interpreter.py: Unit tests for the bcl_interpreter submodule.
"""

import pytest
from bcl_interpreter import interpreter as itp


def __validate_stdout(capsys, *, source: str, expected_stdout: str):
    """Validates that the provided source produces the expected standard output."""

    interpreter = itp.Interpreter(source)
    interpreter.run()

    actual_stdout, _ = capsys.readouterr()

    assert actual_stdout == expected_stdout


def __expect_runtime_error(*, source: str):
    """Validates that the provided source causes a RuntimeError."""

    interpreter = itp.Interpreter(source)

    with pytest.raises(RuntimeError):
        interpreter.run()


def test_empty():
    """Handling an empty source string."""

    interpreter = itp.Interpreter("")

    interpreter.run()
    interpreter.run()
    interpreter.run()


def test_hello_world(capsys):
    """Handling a Hello World program."""

    __validate_stdout(capsys, source='print "Hello World!"', expected_stdout="Hello World!\n")


def test_print(capsys):
    """Handling basic print statements."""

    __validate_stdout(
        capsys,
        source="""
        print "Hello World!"
        """,
        expected_stdout="Hello World!\n",
    )

    __validate_stdout(
        capsys,
        source="""
        print "Policies"
        print "Have"
        print "Risen"
        """,
        expected_stdout="Policies\nHave\nRisen\n",
    )

    __validate_stdout(
        capsys,
        source="""
        print true
        print false
        """,
        expected_stdout="true\nfalse\n",
    )

    __validate_stdout(
        capsys,
        source="""
        print 00
        print 935
        print -75
        """,
        expected_stdout="0\n935\n-75\n",
    )

    __validate_stdout(
        capsys,
        source="""
        print 05.090
        print -3.76
        """,
        expected_stdout="5.09\n-3.76\n",
    )


def test_if_basic(capsys):
    """Handling a basic 'if' statement."""

    __validate_stdout(
        capsys,
        source="""
        if true {
            print "True"
        } else {
            print "False"
        }
        """,
        expected_stdout="True\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if false {
            print "True"
        } else {
            print "False"
        }
        """,
        expected_stdout="False\n",
    )


def test_if_chained(capsys):
    """Testing chained 'if' statements."""

    __validate_stdout(
        capsys,
        source="""
        if true {
            print "1"
        } else if true {
            print "2"
        } else if true {
            print "3"
        } else {
            print "4"
        }
        """,
        expected_stdout="1\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if false {
            print "1"
        } else if true {
            print "2"
        } else if true {
            print "3"
        } else {
            print "4"
        }
        """,
        expected_stdout="2\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if false {
            print "1"
        } else if false {
            print "2"
        } else if true {
            print "3"
        } else {
            print "4"
        }
        """,
        expected_stdout="3\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if false {
            print "1"
        } else if false {
            print "2"
        } else if false {
            print "3"
        } else {
            print "4"
        }
        """,
        expected_stdout="4\n",
    )


def test_if_nested(capsys):
    """Handling nested 'if' statements."""

    __validate_stdout(
        capsys,
        source="""
        if true {
            if true {
                print "1"
            } else {
                print "2"
            }
        } else {
            if true {
                print "3"
            } else {
                print "4"
            }
        }
        """,
        expected_stdout="1\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if true {
            if false {
                print "1"
            } else {
                print "2"
            }
        } else {
            if true {
                print "3"
            } else {
                print "4"
            }
        }
        """,
        expected_stdout="2\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if false {
            if true {
                print "1"
            } else {
                print "2"
            }
        } else {
            if true {
                print "3"
            } else {
                print "4"
            }
        }
        """,
        expected_stdout="3\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if false {
            if true {
                print "1"
            } else {
                print "2"
            }
        } else {
            if false {
                print "3"
            } else {
                print "4"
            }
        }
        """,
        expected_stdout="4\n",
    )


def test_if_consecutive(capsys):
    """Handling consecutive 'if' statements."""

    __validate_stdout(
        capsys,
        source="""
        if true { print "1" }
        if true { print "2" }
        if false { print "3" }
        if true { print "4" }
        if false { print "5" }
        """,
        expected_stdout="1\n2\n4\n",
    )


def test_if_expressions(capsys):
    """Handling different expression types within 'if' statements."""

    __validate_stdout(
        capsys,
        source="""
        if "Non-empty string" { print "1" }
        if "" { print "2" }
        """,
        expected_stdout="1\n",
    )

    __validate_stdout(
        capsys,
        source="""
        if 1 { print "1" }
        if 6 { print "2" }
        if 0 { print "3" }

        if 1.1 { print "4" }
        if 0.0 { print "5" }
        """,
        expected_stdout="1\n2\n4\n",
    )

    __validate_stdout(
        capsys,
        source="""
        let var1 = true
        if var1 { print "1" } else { print "2" }

        let var2 = ""
        if var2 { print "3" } else { print "4"}

        let var3 = 3.3
        if var3 { print "5" } else { print "6" }
        """,
        expected_stdout="1\n4\n5\n",
    )


def test_variable_declaration(capsys):
    """Handling basic variable declarations."""

    __validate_stdout(
        capsys,
        source="""
        let my_var = "Hello Duckie"
        print my_var
        """,
        expected_stdout="Hello Duckie\n",
    )

    __validate_stdout(
        capsys,
        source="""
        let var1 = "Hello Matt"
        let var2 = var1
        let var3 = var2
        print var3
        """,
        expected_stdout="Hello Matt\n",
    )

    __expect_runtime_error(
        source="""
        let var1 = "Hello"
        let var1 = "World"
        """,
    )

    __expect_runtime_error(
        source="""
        print variable
        """,
    )


def test_variable_redefinition(capsys):
    """Handling basic variable redefinition."""

    __expect_runtime_error(
        source="""
        variable = "MUSE"
        """,
    )

    __validate_stdout(
        capsys,
        source="""
        let variable = "Take"
        print variable

        variable = "A"
        print variable

        variable = "Bow"
        print variable
        """,
        expected_stdout="Take\nA\nBow\n",
    )


def test_code_blocks(capsys):
    """Handling code blocks."""

    __validate_stdout(
        capsys,
        source="""
        let variable = "Starlight"

        {
            variable = "Madness"
        }

        print variable
        """,
        expected_stdout="Madness\n",
    )


def test_variable_scoping(capsys):
    """Handling variables within different scopes."""

    __validate_stdout(
        capsys,
        source="""
        let variable = "Out"
        print variable

        {
            print variable

            variable = "In"
            print variable
        }

        print variable
        """,
        expected_stdout="Out\nOut\nIn\nIn\n",
    )

    __validate_stdout(
        capsys,
        source="""
        let variable = "Out"
        print variable

        {
            print variable

            let variable = "In"
            print variable
        }

        print variable
        """,
        expected_stdout="Out\nOut\nIn\nOut\n",
    )

    __expect_runtime_error(
        source="""
        {
            let variable = "In"
        }

        print variable
        """
    )

    __expect_runtime_error(
        source="""
        {
            let variable = "First"
        }

        {
            variable = "Second"
        }
        """
    )

    __validate_stdout(
        capsys,
        source="""
        let var1 = 1
        let var2 = 2

        if true {
            var1 = 100
        } else {
            var2 = 200
        }

        print var1
        print var2
        """,
        expected_stdout="100\n2\n",
    )

    __validate_stdout(
        capsys,
        source="""
        let variable = 1

        {
            let variable = 2

            {
                variable = 3
                print variable
            }

            print variable
        }

        print variable
        """,
        expected_stdout="3\n3\n1\n",
    )

    __expect_runtime_error(
        source="""
        if false {
            let variable = "The Dark Side"
        }

        print variable
        """
    )


def test_while_loop_no_runs(capsys):
    """Handling a while loop that never runs."""

    __validate_stdout(
        capsys,
        source="""
        while false {
            print "No"
        }
        """,
        expected_stdout="",
    )


def test_while_loop_runs_once(capsys):
    """Handling a while loop that runs once."""

    __validate_stdout(
        capsys,
        source="""
        let expression = true

        while expression {
            print "Run"
            expression = false
        }
        """,
        expected_stdout="Run\n",
    )


def test_while_loop_runs_twice(capsys):
    """Handling a while loop that runs twice."""

    __validate_stdout(
        capsys,
        source="""
        let expression1 = true
        let expression2 = true

        while expression1 {
            print "Run"
            if expression2 {
                expression2 = false
            } else {
                expression1 = false
            }
        }
        """,
        expected_stdout="Run\nRun\n",
    )


def test_sum_two_integers(capsys):
    """Handling addition of two integers."""

    __validate_stdout(
        capsys,
        source="""
        let x = 1 + 2
        print x
        """,
        expected_stdout="3\n",
    )


def test_sum_three_integers(capsys):
    """Handling addition of two integers."""

    __validate_stdout(
        capsys,
        source="""
        let x = 1 + 2 + 3
        print x
        """,
        expected_stdout="6\n",
    )


def test_sum_two_floats(capsys):
    """Handling addition of two floats."""

    __validate_stdout(
        capsys,
        source="""
        let x = 1.125 + 2.25
        print x
        """,
        expected_stdout="3.375\n",
    )


def test_sum_three_floats(capsys):
    """Handling addition of two floats."""

    __validate_stdout(
        capsys,
        source="""
        let x = 1.125 + 2.125 + 3.25
        print x
        """,
        expected_stdout="6.5\n",
    )


def test_sum_integer_and_float(capsys):
    """Handling addition of an integer and a float."""

    __validate_stdout(
        capsys,
        source="""
        let x = 6 + 1.25
        print x
        """,
        expected_stdout="7.25\n",
    )


def test_subtract_two_integers(capsys):
    """Handling subtraction of two integers."""

    __validate_stdout(
        capsys,
        source="""
        let x = 6 - 1
        print x
        """,
        expected_stdout="5\n",
    )


def test_subtract_two_floats(capsys):
    """Handling subtraction of two floats."""

    __validate_stdout(
        capsys,
        source="""
        let x = 6.75 - 1.25
        print x
        """,
        expected_stdout="5.5\n",
    )


def test_subtract_three_numbers(capsys):
    """Handling subtraction of three numbers (floats/integers)."""

    __validate_stdout(
        capsys,
        source="""
        let x = 6 - 1 - 2.5
        print x
        """,
        expected_stdout="2.5\n",
    )
