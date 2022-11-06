"""
Contains the TOKEN_REGEXPS dictionary.
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
    r"^-?[0-9]+(\.[0-9]+)?\b": "NUMBER",
    # String literals
    r'^"[^"]*"': "STRING",
    # Boolean literals
    r"^true\b|^false\b": "BOOLEAN",
    # ==================== Keywords ====================
    # Keyword "let"
    r"^let\b": "LET",
    # Keyword "func"
    r"^func\b": "FUNC",
    # Keyword "print"
    r"^print\b": "PRINT",
    # Keyword "if"
    r"^if\b": "IF",
    # Keyword "else"
    r"^else\b": "ELSE",
    # Keyword "while"
    r"^while\b": "WHILE",
    # ==================== Operators ====================
    # Equality Operator
    r"^==": "==",
    # Inequality Operator
    r"^!=": "!=",
    # Less Than Or Equal Operator
    r"^<=": "<=",
    # Less Than Operator
    r"^<": "<",
    # Assignment Operator
    r"^=": "=",
    # Plus Operator
    r"^\+": "+",
    # Subtract Operator
    r"^-": "-",
    # Multiply Operator
    r"^\*": "*",
    # Divide Operator
    r"^/": "/",
    # ==================== Identifiers ====================
    # Identifiers (function names, variables, classes, etc)
    r"^[a-z][a-z0-9_]*\b": "IDENTIFIER",
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
