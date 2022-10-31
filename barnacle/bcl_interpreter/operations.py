"""
operations.py: Supported operators and their operands for Barnacle.

This includes mathematical operators such as +, -, *, / and boolean operators like `not` and `or`.
"""


from typing import Any


def calculate_binary_operation(operator: str, left: Any, right: Any) -> Any:
    """
    Perform an operation on two operands.
    Raises an exception if the given operation and operands are not supported.
    """

    match (operator, left, right):
        case ("==", l, r) if type(l) == type(r):
            return left == right

        case ("+", int() | float(), int() | float()):
            return left + right
        case ("+", str(), str()):
            return left + right

        case ("-", int() | float(), int() | float()):
            return left - right
        case ("-", str(), str()):
            return __remove_trailing_substring(left=left, right=right)

        case ("*", int() | float(), int() | float()):
            return left * right

        case ("/", int() | float(), int() | float()):
            return left / right


    raise RuntimeError(
        f"Operator '{operator}' does not support the provided operand types "
        f"'{type(left).__name__}' and '{type(right).__name__}'"
    )


def __remove_trailing_substring(left: str, right: str) -> str:
    """Remove a trailing substring from a string."""

    if not left.endswith(right):
        raise RuntimeError(
            f"Error subtracting strings: Trailing substring '{right}' does not exist in the primary string '{left}'"
        )

    return left[0 : -len(right)]
