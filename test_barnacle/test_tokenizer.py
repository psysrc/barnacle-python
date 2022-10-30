"""
test_tokenizer.py: Unit tests for the bcl_tokenizer submodule.
"""

from bcl_tokenizer import tokenizer as tkn


def __verify_first_token(source: str, expected_type: str, expected_value: str):
    """Verify that the first token produced by the tokenized source has the expected type and value."""

    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.end_of_stream()

    actual_first_token = tokenizer.next_token()
    assert actual_first_token == {"type": expected_type, "value": expected_value}


def __verify_token(source: str, expected_token: dict):
    """Verify that the source produces exactly one token which matches the expected token when tokenized."""

    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.end_of_stream()

    actual_token = tokenizer.next_token()

    assert tokenizer.end_of_stream()
    assert tokenizer.next_token() is None

    assert actual_token == expected_token


def __verify_token_basic(source: str, expected_token_type: str):
    """
    Verify that the source produces exactly one token which, when tokenized:

    - Has the expected token type.
    - Has a value matching exactly the source.
    """

    __verify_token(source, {"type": expected_token_type, "value": source})


def __verify_not_token_type(source: str, unexpected_token_type: str):
    """Verify that the source does NOT produce the provided token type when tokenized."""

    tokenizer = tkn.Tokenizer(source)

    try:
        while token := tokenizer.next_token():
            assert token["type"] != unexpected_token_type, token

    except SyntaxError:
        pass


def test_empty():
    """Handling an empty source string."""

    tokenizer = tkn.Tokenizer("")

    assert tokenizer.end_of_stream()
    assert tokenizer.next_token() is None


def test_whitespace():
    """Handling source that is only whitespace."""

    source = "         \n      \n\n\t\n \n \r\n \r      \r\n\r \t     \t \t\r\t\r\n"

    __verify_token(source, None)


def test_comments():
    """Handling source that is only comments."""

    source = """\
// This is a comment
// empty comment below
//

/* Block comment - empty block comments below */
/**//**//**/
/* Multi-line
    block comment!
    Still going
*/

/* Single-line comment inside a block comment
    // here it is
*/

// Block comment inside a single-line comment /* hello */
"""

    __verify_token(source, None)


def test_number_literals():
    """Handling number literals."""

    __verify_token_basic("0", "NUMBER")
    __verify_token_basic("1", "NUMBER")
    __verify_token_basic("6", "NUMBER")
    __verify_token_basic("10", "NUMBER")
    __verify_token_basic("11", "NUMBER")
    __verify_token_basic("00", "NUMBER")
    __verify_token_basic("00000", "NUMBER")
    __verify_token_basic("05", "NUMBER")
    __verify_token_basic("024", "NUMBER")
    __verify_token_basic("298754", "NUMBER")
    __verify_token_basic("105", "NUMBER")
    __verify_token_basic("76485658457485", "NUMBER")
    __verify_token_basic("3286592", "NUMBER")

    __verify_token_basic("-1", "NUMBER")
    __verify_token_basic("-0", "NUMBER")
    __verify_token_basic("-13", "NUMBER")
    __verify_token_basic("-835623", "NUMBER")
    __verify_token_basic("-65987265795785", "NUMBER")

    __verify_token_basic("1.1", "NUMBER")
    __verify_token_basic("1.0", "NUMBER")
    __verify_token_basic("0.1", "NUMBER")
    __verify_token_basic("0.0", "NUMBER")
    __verify_token_basic("87.69", "NUMBER")
    __verify_token_basic("9832.7745756892246", "NUMBER")
    __verify_token_basic("000287650.0002865832000", "NUMBER")

    __verify_token_basic("-0.1", "NUMBER")
    __verify_token_basic("-0.0", "NUMBER")
    __verify_token_basic("-87.69", "NUMBER")
    __verify_token_basic("-9832.7745756892246", "NUMBER")
    __verify_token_basic("-000287650.0002865832000", "NUMBER")

    __verify_not_token_type("b1", "NUMBER")
    __verify_not_token_type("B1", "NUMBER")
    __verify_not_token_type("1b", "NUMBER")
    __verify_not_token_type("1B", "NUMBER")
    __verify_not_token_type("i6", "NUMBER")
    __verify_not_token_type("l8", "NUMBER")
    __verify_not_token_type("L8", "NUMBER")
    __verify_not_token_type("u3", "NUMBER")
    __verify_not_token_type("U3", "NUMBER")


def test_string_literals():
    """Handling string literals."""

    __verify_token_basic('""', "STRING")
    __verify_token_basic('"Hi"', "STRING")
    __verify_token_basic('"Hello World!"', "STRING")
    __verify_token_basic('"Whoops\nI\nDid\nIt\nAgain"', "STRING")
    __verify_token_basic('"Whoops\r\nI\r\nDid\r\nIt\r\nAgain\r\n(Windows)"', "STRING")
    __verify_token_basic('"A comment looks like /* this */"', "STRING")
    __verify_token_basic('"A comment looks like // this"', "STRING")
    __verify_token_basic('"12"', "STRING")
    __verify_token_basic('"14.09"', "STRING")

    __verify_not_token_type("''", "STRING")
    __verify_not_token_type("'Hi'", "STRING")
    __verify_not_token_type("'Hello World!'", "STRING")
    __verify_not_token_type("Hi", "STRING")
    __verify_not_token_type('"Where is the other quote mark?', "STRING")

    __verify_first_token('"Big F"\n', "STRING", '"Big F"')
    __verify_first_token('"Big F"\r\n', "STRING", '"Big F"')
    __verify_first_token('"Big F" ', "STRING", '"Big F"')


def test_boolean_literals():
    """Handling boolean literals."""

    __verify_token_basic("true", "BOOLEAN")
    __verify_token_basic("false", "BOOLEAN")

    __verify_not_token_type("truey", "BOOLEAN")
    __verify_not_token_type("true9", "BOOLEAN")
    __verify_not_token_type("tru evt", "BOOLEAN")
    __verify_not_token_type("falsey", "BOOLEAN")
    __verify_not_token_type("fal sed", "BOOLEAN")

    __verify_first_token("true{", "BOOLEAN", "true")
    __verify_first_token("true}", "BOOLEAN", "true")
    __verify_first_token("true(", "BOOLEAN", "true")
    __verify_first_token("true)", "BOOLEAN", "true")
    __verify_first_token("true ", "BOOLEAN", "true")
    __verify_first_token("true\n", "BOOLEAN", "true")
    __verify_first_token("true\r\n", "BOOLEAN", "true")
    __verify_first_token("false{", "BOOLEAN", "false")
    __verify_first_token("false}", "BOOLEAN", "false")
    __verify_first_token("false(", "BOOLEAN", "false")
    __verify_first_token("false)", "BOOLEAN", "false")
    __verify_first_token("false ", "BOOLEAN", "false")
    __verify_first_token("false\n", "BOOLEAN", "false")
    __verify_first_token("false\r\n", "BOOLEAN", "false")


def test_keyword_let():
    """Handling the LET keyword."""

    __verify_token_basic("let", "LET")

    __verify_not_token_type("letty", "LET")

    __verify_first_token("let ", "LET", "let")


def test_keyword_while():
    """Handling the WHILE keyword."""

    __verify_token_basic("while", "WHILE")

    __verify_not_token_type("whiley", "WHILE")

    __verify_first_token("while ", "WHILE", "while")


def test_identifiers():
    """Handling identifiers."""

    __verify_token_basic("my_variable", "IDENTIFIER")
    __verify_token_basic("some_2nd_variable", "IDENTIFIER")
    __verify_token_basic("unreadablebutvalid", "IDENTIFIER")
    __verify_token_basic("i", "IDENTIFIER")
    __verify_token_basic("j", "IDENTIFIER")
    __verify_token_basic("x", "IDENTIFIER")

    __verify_not_token_type("CONST_VALUE", "IDENTIFIER")
    __verify_not_token_type("no_uppercase_Letters", "IDENTIFIER")

    __verify_not_token_type("_no_starting_underscores", "IDENTIFIER")
    __verify_not_token_type("1_no_starting_numbers", "IDENTIFIER")

    __verify_not_token_type("true", "IDENTIFIER")
    __verify_not_token_type("false", "IDENTIFIER")
    __verify_not_token_type("let", "IDENTIFIER")
    __verify_not_token_type("print", "IDENTIFIER")
    __verify_not_token_type("while", "IDENTIFIER")
    __verify_not_token_type("if", "IDENTIFIER")


def test_operator_plus():
    """Handling the + operator."""

    __verify_token_basic("+", "+")

    __verify_first_token("+ ", "+", "+")
    __verify_first_token("+ 6", "+", "+")
    __verify_first_token('+ "World"', "+", "+")


def test_operator_subtract():
    """Handling the - operator."""

    __verify_token_basic("-", "-")

    __verify_first_token("- ", "-", "-")
    __verify_first_token("- 2", "-", "-")
    __verify_first_token('- "World"', "-", "-")
