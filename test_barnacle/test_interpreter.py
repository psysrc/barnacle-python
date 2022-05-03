"""
test_interpreter.py: Unit tests for the bcl_interpreter submodule.
"""

from bcl_interpreter import interpreter as itp


def test_empty():
    """Handling an empty source string."""

    interpreter = itp.Interpreter("")

    interpreter.run()
    interpreter.run()
    interpreter.run()
