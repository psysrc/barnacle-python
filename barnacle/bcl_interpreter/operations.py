"""
Supported operators and their operands for Barnacle.

This includes mathematical operators such as +, -, *, / and boolean operators like `not` and `or`.
"""


from typing import Any


class OperationNotSupported(RuntimeError):
    """Exception thrown when an unsupported operation is attempted."""


def calculate_binary_operation(operator: str, left: Any, right: Any) -> Any:
    """
    Perform an operation on two operands.
    Raises an exception if the given operation and operands are not supported.
    """

    # Lots of return statements here because it works well with the match-case
    # pylint: disable=too-many-return-statements

    l_type = type(left)
    r_type = type(right)

    match (operator, left, right):
        case ("==", _, _) if l_type == r_type:
            return left == right
        case ("==", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left == right

        case ("!=", _, _) if l_type == r_type:
            return left != right
        case ("!=", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left != right

        case ("<", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left < right

        case ("<=", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left <= right

        case ("+", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left + right
        case ("+", str(), str()):
            return left + right

        case ("-", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left - right
        case ("-", str(), str()):
            return __remove_trailing_substring(left=left, right=right)

        case ("*", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left * right

        case ("/", _, _) if l_type in [int, float] and r_type in [int, float]:
            return left / right

    raise OperationNotSupported(
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
