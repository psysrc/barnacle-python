"""
Unit tests for the basic functionality of the bcl_interpreter submodule.
"""

from bcl_interpreter import interpreter as itp

from .interpreter_helpers import expect_error, validate_stdout


def test_empty():
    """Handling an empty source string."""

    interpreter = itp.Interpreter("")

    interpreter.run()
    interpreter.run()
    interpreter.run()


def test_hello_world(capsys):
    """Handling a Hello World program."""

    validate_stdout(capsys, source='print "Hello World!"', expected_stdout="Hello World!\n")


def test_print(capsys):
    """Handling basic print statements."""

    validate_stdout(
        capsys,
        source="""
        print "Hello World!"
        """,
        expected_stdout="Hello World!\n",
    )

    validate_stdout(
        capsys,
        source="""
        print "Policies"
        print "Have"
        print "Risen"
        """,
        expected_stdout="Policies\nHave\nRisen\n",
    )

    validate_stdout(
        capsys,
        source="""
        print true
        print false
        """,
        expected_stdout="true\nfalse\n",
    )

    validate_stdout(
        capsys,
        source="""
        print 00
        print 935
        print -75
        """,
        expected_stdout="0\n935\n-75\n",
    )

    validate_stdout(
        capsys,
        source="""
        print 05.090
        print -3.76
        """,
        expected_stdout="5.09\n-3.76\n",
    )


def test_if_basic(capsys):
    """Handling a basic 'if' statement."""

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
        capsys,
        source="""
        if "Non-empty string" { print "1" }
        if "" { print "2" }
        """,
        expected_stdout="1\n",
    )

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
        capsys,
        source="""
        let my_var = "Hello Duckie"
        print my_var
        """,
        expected_stdout="Hello Duckie\n",
    )

    validate_stdout(
        capsys,
        source="""
        let var1 = "Hello Matt"
        let var2 = var1
        let var3 = var2
        print var3
        """,
        expected_stdout="Hello Matt\n",
    )

    expect_error(
        source="""
        let var1 = "Hello"
        let var1 = "World"
        """,
        exception=RuntimeError,
    )

    expect_error(
        source="""
        print variable
        """,
        exception=RuntimeError,
    )


def test_variable_redefinition(capsys):
    """Handling basic variable redefinition."""

    expect_error(
        source="""
        variable = "MUSE"
        """,
        exception=RuntimeError,
    )

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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

    expect_error(
        source="""
        {
            let variable = "In"
        }

        print variable
        """,
        exception=RuntimeError,
    )

    expect_error(
        source="""
        {
            let variable = "First"
        }

        {
            variable = "Second"
        }
        """,
        exception=RuntimeError,
    )

    validate_stdout(
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

    validate_stdout(
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

    expect_error(
        source="""
        if false {
            let variable = "The Dark Side"
        }

        print variable
        """,
        exception=RuntimeError,
    )


def test_while_loop_no_runs(capsys):
    """Handling a while loop that never runs."""

    validate_stdout(
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

    validate_stdout(
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

    validate_stdout(
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


def test_string_concatenation_string_literals(capsys):
    """Handling string concatenation with two string literals."""

    validate_stdout(
        capsys,
        source="""
        let x = "Hello" + " World"
        print x
        """,
        expected_stdout="Hello World\n",
    )


def test_string_concatenation_string_literal_and_variable(capsys):
    """Handling string concatenation with two string literals."""

    validate_stdout(
        capsys,
        source="""
        let x = "Hi"
        let y = x + " Dad"
        print y
        """,
        expected_stdout="Hi Dad\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = " Mum"
        let y = "Hi" + x
        print y
        """,
        expected_stdout="Hi Mum\n",
    )


def test_string_concatenation_two_variables(capsys):
    """Handling string concatenation with two variables."""

    validate_stdout(
        capsys,
        source="""
        let x = "Good"
        let y = " Morning"
        let z = x + y
        print z
        """,
        expected_stdout="Good Morning\n",
    )


def test_string_truncation_literal_and_variable(capsys):
    """Handling string truncation with a string literal and a variable."""

    validate_stdout(
        capsys,
        source="""
        let x = "AlphaBetaGamma"
        let y = x - "Gamma"
        print y
        """,
        expected_stdout="AlphaBeta\n",
    )


def test_bad_string_truncation():
    """Handling bad string truncation."""

    expect_error(
        source="""
        let x = "AlphaBetaGamma"
        let y = x - "Zeta"
        """,
        exception=RuntimeError,
    )


def test_do_while_loop_runs_once(capsys):
    """Handling a do-while loop that runs once."""

    validate_stdout(
        capsys,
        source="""
        do {
            print "Run"
        } while false
        """,
        expected_stdout="Run\n",
    )


def test_do_while_loop_runs_twice(capsys):
    """Handling a do-while loop that runs twice."""

    validate_stdout(
        capsys,
        source="""
        let x = 2

        do {
            print "Run"
            x = x - 1
        } while x > 0
        """,
        expected_stdout="Run\nRun\n",
    )

