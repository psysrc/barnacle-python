"""
Unit tests for the comparison functionality of the bcl_interpreter submodule.
"""

from bcl_interpreter.operations import OperationNotSupported

from .interpreter_helpers import expect_error, validate_stdout


def test_equality_string_and_variable(capsys):
    """Handling equality between a variable and a string literal."""

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let eq = x == "Alpha"
        print eq
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let eq = x == "Beta"
        print eq
        """,
        expected_stdout="false\n",
    )


def test_equality_bool_and_variable(capsys):
    """Handling equality between a variable and a boolean literal."""

    validate_stdout(
        capsys,
        source="""
        let x = true
        let eq = x == true
        print eq
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = true
        let eq = x == false
        print eq
        """,
        expected_stdout="false\n",
    )


def test_equality_integer_and_variable(capsys):
    """Handling equality between a variable and an integer literal."""

    validate_stdout(
        capsys,
        source="""
        let x = 12
        let eq = x == 12
        print eq
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 12
        let eq = x == 4
        print eq
        """,
        expected_stdout="false\n",
    )


def test_equality_float_and_variable(capsys):
    """Handling equality between a variable and a float literal."""

    validate_stdout(
        capsys,
        source="""
        let x = 12.3
        let eq = x == 12.3
        print eq
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 12.3
        let eq = x == 9.1
        print eq
        """,
        expected_stdout="false\n",
    )


def test_equality_two_variables(capsys):
    """Handling equality between two variables."""

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let y = "Alpha"
        let eq = x == y
        print eq
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let y = "Beta"
        let eq = x == y
        print eq
        """,
        expected_stdout="false\n",
    )


def test_equality_two_variables_different_types():
    """Handling equality between two variables containing different types."""

    expect_error(
        source="""
        let x = "Alpha"
        let y = 7
        let eq = x == y
        """,
        exception=OperationNotSupported,
    )

    expect_error(
        source="""
        let x = false
        let y = 7.8
        let eq = x == y
        """,
        exception=OperationNotSupported,
    )


def test_inequality_string_and_variable(capsys):
    """Handling inequality between a variable and a string literal."""

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let eq = x != "Alpha"
        print eq
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let eq = x != "Beta"
        print eq
        """,
        expected_stdout="true\n",
    )


def test_inequality_bool_and_variable(capsys):
    """Handling inequality between a variable and a boolean literal."""

    validate_stdout(
        capsys,
        source="""
        let x = true
        let eq = x != true
        print eq
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = true
        let eq = x != false
        print eq
        """,
        expected_stdout="true\n",
    )


def test_inequality_integer_and_variable(capsys):
    """Handling inequality between a variable and an integer literal."""

    validate_stdout(
        capsys,
        source="""
        let x = 12
        let eq = x != 12
        print eq
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 12
        let eq = x != 4
        print eq
        """,
        expected_stdout="true\n",
    )


def test_inequality_float_and_variable(capsys):
    """Handling inequality between a variable and a float literal."""

    validate_stdout(
        capsys,
        source="""
        let x = 12.3
        let eq = x != 12.3
        print eq
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 12.3
        let eq = x != 9.1
        print eq
        """,
        expected_stdout="true\n",
    )


def test_inequality_two_variables(capsys):
    """Handling inequality between two variables."""

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let y = "Alpha"
        let eq = x != y
        print eq
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = "Alpha"
        let y = "Beta"
        let eq = x != y
        print eq
        """,
        expected_stdout="true\n",
    )


def test_inequality_two_variables_different_types():
    """Handling inequality between two variables containing different types."""

    expect_error(
        source="""
        let x = "Alpha"
        let y = 7
        let eq = x != y
        """,
        exception=OperationNotSupported,
    )

    expect_error(
        source="""
        let x = false
        let y = 7.8
        let eq = x != y
        """,
        exception=OperationNotSupported,
    )


def test_equality_float_and_integer(capsys):
    """Handling equality between a float and an integer."""

    validate_stdout(
        capsys,
        source="""
        let x = 1
        let y = 1.0
        let eq = x == y
        print eq
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 4
        let y = 9.9
        let eq = x == y
        print eq
        """,
        expected_stdout="false\n",
    )


def test_inequality_float_and_integer(capsys):
    """Handling inequality between a float and an integer."""

    validate_stdout(
        capsys,
        source="""
        let x = 1
        let y = 1.0
        let eq = x != y
        print eq
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 4
        let y = 9.9
        let eq = x != y
        print eq
        """,
        expected_stdout="true\n",
    )


def test_less_than_integer_and_integer_variable(capsys):
    """Handling the less-than operator between an integer literal and an integer variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x < 8
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x < 3
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x < 5
        print lt
        """,
        expected_stdout="false\n",
    )


def test_less_than_integer_and_float_variable(capsys):
    """Handling the less-than operator between an integer literal and an float variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x < 8
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x < 3
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x < 5.5
        print lt
        """,
        expected_stdout="false\n",
    )


def test_less_than_does_not_support_booleans():
    """Handling the less-than operator with booleans."""

    expect_error(
        source="""
        let x = true
        let oof = x < 5
        """,
        exception=OperationNotSupported,
    )

    expect_error(
        source="""
        let x = false
        let oof = 3 < x
        """,
        exception=OperationNotSupported,
    )


def test_less_than_or_equal_integer_and_integer_variable(capsys):
    """Handling the less-than-or-equal operator between an integer literal and an integer variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x <= 8
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x <= 3
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x <= 5
        print lt
        """,
        expected_stdout="true\n",
    )


def test_less_than_or_equal_integer_and_float_variable(capsys):
    """Handling the less-than-or-equal operator between an integer literal and an float variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x <= 8
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x <= 3
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x <= 5.5
        print lt
        """,
        expected_stdout="true\n",
    )


def test_less_than_or_equal_does_not_support_booleans():
    """Handling the less-than-or-equal operator with booleans."""

    expect_error(
        source="""
        let x = true
        let oof = x <= 5
        """,
        exception=OperationNotSupported,
    )

    expect_error(
        source="""
        let x = false
        let oof = 3 <= x
        """,
        exception=OperationNotSupported,
    )


def test_more_than_integer_and_integer_variable(capsys):
    """Handling the more-than operator between an integer literal and an integer variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x > 8
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x > 3
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x > 5
        print lt
        """,
        expected_stdout="false\n",
    )


def test_more_than_integer_and_float_variable(capsys):
    """Handling the more-than operator between an integer literal and an float variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x > 8
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x > 3
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x > 5.5
        print lt
        """,
        expected_stdout="false\n",
    )


def test_more_than_does_not_support_booleans():
    """Handling the more-than operator with booleans."""

    expect_error(
        source="""
        let x = true
        let oof = x > 5
        """,
        exception=OperationNotSupported,
    )

    expect_error(
        source="""
        let x = false
        let oof = 3 > x
        """,
        exception=OperationNotSupported,
    )


def test_more_than_or_equal_integer_and_integer_variable(capsys):
    """Handling the more-than-or-equal operator between an integer literal and an integer variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x >= 8
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x >= 3
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5
        let lt = x >= 5
        print lt
        """,
        expected_stdout="true\n",
    )


def test_more_than_or_equal_integer_and_float_variable(capsys):
    """Handling the more-than-or-equal operator between an integer literal and an float variable."""

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x >= 8
        print lt
        """,
        expected_stdout="false\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x >= 3
        print lt
        """,
        expected_stdout="true\n",
    )

    validate_stdout(
        capsys,
        source="""
        let x = 5.5
        let lt = x >= 5.5
        print lt
        """,
        expected_stdout="true\n",
    )


def test_more_than_or_equal_does_not_support_booleans():
    """Handling the more-than-or-equal operator with booleans."""

    expect_error(
        source="""
        let x = true
        let oof = x >= 5
        """,
        exception=OperationNotSupported,
    )

    expect_error(
        source="""
        let x = false
        let oof = 3 >= x
        """,
        exception=OperationNotSupported,
    )
