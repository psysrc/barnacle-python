"""
tokens.py: Contains the TOKEN_REGEXPS dictionary.
"""

TOKEN_REGEXPS = {
    # Key-value pairs represent a token regex and its corresponding token type
    # A token type of None means the pseudo-token should be ignored (e.g. whitespace or comments)
    # Order is important! Even if multiple regexes would match a token, the higher one in this dict takes precedence.
    # ==================== Ignore ====================
    # Whitespace (ignore)
    r"^\s": None,
    # Block comments (ignore)
    r"^/\*(.|\n)*?\*/": None,
    # Single-line comments (ignore)
    r"^//.*": None,
    # ==================== Literals ====================
    # Number literals
    r"^-?[0-9]+(\.[0-9]+)?": "NUMBER",
    # String literals
    r'^"[^"]*"': "STRING",
    # Boolean literals
    r"^true\s|^false\s": "BOOLEAN",
    # ==================== Keywords ====================
    # Keyword "let"
    r"^let\s": "LET",
    # Keyword "func"
    r"^func\s": "FUNC",
    # Keyword "print"
    r"^print\s": "PRINT",
    # Keyword "if"
    r"^if\s": "IF",
    # Keyword "else"
    r"^else\s": "ELSE",
    # ==================== Operators ====================
    # Assignment Operator
    r"^=": "ASSIGN_OP",
    # ==================== Identifiers ====================
    # Identifiers (function names, variables, classes, etc)
    r"^[a-z][a-z0-9_]+": "IDENTIFIER",
    # ==================== Miscellaneous ====================
    # Braces
    r"^{": "{",
    r"^}": "}",
    # Parentheses
    r"^\(": "(",
    r"^\)": ")",
    # Commas
    r"^,": ",",
}
