"""
Implements helper functions for the bcl_interpreter unit tests.
"""

import pytest
from bcl_interpreter import interpreter as itp


def validate_stdout(capsys, *, source: str, expected_stdout: str):
    """Validates that the provided source produces the expected standard output."""

    interpreter = itp.Interpreter(source)
    interpreter.run()

    actual_stdout, _ = capsys.readouterr()

    assert actual_stdout == expected_stdout


def expect_error(*, source: str, exception: Exception):
    """Validates that the provided source causes a specific exception."""

    interpreter = itp.Interpreter(source)

    with pytest.raises(exception):
        interpreter.run()
