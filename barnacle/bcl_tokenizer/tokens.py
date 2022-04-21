TOKEN_REGEXPS = {
    # Key-value pairs represent a token regex and its corresponding token type
    # A token type of None means the pseudo-token should be ignored (e.g. whitespace or comments)

    # ==================== Ignore ====================
    # Whitespace (ignore)
    "^\s": None,

    # Block comments (ignore)
    "^/\*(.|\n)*?\*/": None,

    # Single-line comments (ignore)
    "^//.*": None,

    # ==================== Literals ====================
    # Number literals
    "^[0-9]+(\.[0-9]+)?": "NUMBER",

    # String literals
    "^\"[^\"]*\"": "STRING",

    # ==================== Keywords ====================
    # Keyword "LET"
    "^LET ": "LET",

    # Keyword "PRINT"
    "^PRINT ": "PRINT",

    # ==================== Operators ====================
    # Assignment Operator
    "^=": "ASSIGN_OP",

    # ==================== Identifiers ====================
    # Identifiers (function names, variables, classes, etc)
    "^[a-z][a-z0-9_]+": "IDENTIFIER",
}