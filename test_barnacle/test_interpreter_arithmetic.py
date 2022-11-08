"""
Unit tests for the arithmetic functionality of the bcl_interpreter submodule.
"""

from bcl_interpreter.operations import OperationNotSupported
from .interpreter_helpers import expect_error, validate_stdout


def test_sum_two_integers(capsys):
    """Handling addition of two integers."""

    validate_stdout(
        capsys,
        source="""
        let x = 1 + 2
        print x
        """,
        expected_stdout="3\n",
    )


def test_sum_three_integers(capsys):
    """Handling addition of two integers."""

    validate_stdout(
        capsys,
        source="""
        let x = 1 + 2 + 3
        print x
        """,
        expected_stdout="6\n",
    )


def test_sum_two_floats(capsys):
    """Handling addition of two floats."""

    validate_stdout(
        capsys,
        source="""
        let x = 1.125 + 2.25
        print x
        """,
        expected_stdout="3.375\n",
    )


def test_sum_three_floats(capsys):
    """Handling addition of two floats."""

    validate_stdout(
        capsys,
        source="""
        let x = 1.125 + 2.125 + 3.25
        print x
        """,
        expected_stdout="6.5\n",
    )


def test_sum_integer_and_float(capsys):
    """Handling addition of an integer and a float."""

    validate_stdout(
        capsys,
        source="""
        let x = 6 + 1.25
        print x
        """,
        expected_stdout="7.25\n",
    )


def test_subtract_two_integers(capsys):
    """Handling subtraction of two integers."""

    validate_stdout(
        capsys,
        source="""
        let x = 6 - 1
        print x
        """,
        expected_stdout="5\n",
    )


def test_subtract_two_floats(capsys):
    """Handling subtraction of two floats."""

    validate_stdout(
        capsys,
        source="""
        let x = 6.75 - 1.25
        print x
        """,
        expected_stdout="5.5\n",
    )


def test_subtract_three_numbers(capsys):
    """Handling subtraction of three numbers (floats/integers)."""

    validate_stdout(
        capsys,
        source="""
        let x = 6 - 1 - 2.5
        print x
        """,
        expected_stdout="2.5\n",
    )


def test_multiply_two_integers(capsys):
    """Handling subtraction of two integers."""

    validate_stdout(
        capsys,
        source="""
        let x = 6 * 2
        print x
        """,
        expected_stdout="12\n",
    )


def test_multiply_two_floats(capsys):
    """Handling subtraction of two floats."""

    validate_stdout(
        capsys,
        source="""
        let x = 2.5 * 2.5
        print x
        """,
        expected_stdout="6.25\n",
    )


def test_multiply_two_numbers(capsys):
    """Handling subtraction of two numbers (floats/integers)."""

    validate_stdout(
        capsys,
        source="""
        let x = 6 * 1.5
        print x
        """,
        expected_stdout="9.0\n",
    )


def test_multiplication_has_precedence_over_addition(capsys):
    """Handling multiplication and addition in the same expression."""

    validate_stdout(
        capsys,
        source="""
        let x = 6 * 2 + 4
        print x
        """,
        expected_stdout="16\n",
    )


def test_division_has_precedence_over_subtraction(capsys):
    """Handling division and subtraction in the same expression."""

    validate_stdout(
        capsys,
        source="""
        let x = 6 / 2 - 4
        print x
        """,
        expected_stdout="-1.0\n",
    )

def test_addition_does_not_support_booleans():
    """Handling the + operator with booleans."""

    expect_error(
        source="""
        let x = true
        let oof = x + 1
        """,
        exception=OperationNotSupported,
    )

    expect_error(
        source="""
        let x = false
        let oof = 3 + x
        """,
        exception=OperationNotSupported,
    )
