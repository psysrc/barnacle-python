"""
test_interpreter.py: Unit tests for the bcl_interpreter submodule.
"""

from bcl_interpreter import interpreter as itp


def __validate_stdout(capsys, *, source: str, expected_stdout: str):
    """Validates that the provided source produces the expected standard output."""

    interpreter = itp.Interpreter(source)
    interpreter.run()

    actual_stdout, _ = capsys.readouterr()

    assert actual_stdout == expected_stdout


def test_empty():
    """Handling an empty source string."""

    interpreter = itp.Interpreter("")

    interpreter.run()
    interpreter.run()
    interpreter.run()


def test_hello_world(capsys):
    """Handling a Hello World program."""

    __validate_stdout(capsys, source='print "Hello World!"', expected_stdout="Hello World!\n")


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


def test_variables(capsys):
    """Handling basic variables."""

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
