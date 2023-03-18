"""
Implements the Function dataclass.
"""

from dataclasses import dataclass


@dataclass
class Function:
    """Represents a function that can be interpreted."""

    name: str
    parameters: list[str]
    code_block: dict
