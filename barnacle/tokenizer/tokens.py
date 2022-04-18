TOKEN_REGEXPS = {
    # Key-value pairs represent a token regex and its corresponding token type
    # A token type of None means the pseudo-token should be ignored (e.g. whitespace or comments)

    # Whitespace (ignore)
    "^\s": None,

    # Block comments (ignore)
    "^/\*(.|\n)*?\*/": None,

    # Single-line comments (ignore)
    "^//.*": None,

    # Integers
    "^[0-9]+": "INTEGER",

    # Strings
    "^\"[^\"]*\"": "STRING",
}
