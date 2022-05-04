"""
test_tokenizer.py: Unit tests for the bcl_tokenizer submodule.
"""

from bcl_tokenizer import tokenizer as tkn


def __verify_token(source: str, expected_token: dict):
    """Verify that the source produces exactly one token which matches the expected token when tokenized."""

    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.end_of_stream()

    actual_token = tokenizer.next_token()

    assert tokenizer.end_of_stream()
    assert tokenizer.next_token() is None

    assert actual_token == expected_token


def __verify_token_type(source: str, expected_token_type: str):
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

    __verify_token_type("0", "NUMBER")
    __verify_token_type("1", "NUMBER")
    __verify_token_type("6", "NUMBER")
    __verify_token_type("10", "NUMBER")
    __verify_token_type("11", "NUMBER")
    __verify_token_type("00", "NUMBER")
    __verify_token_type("00000", "NUMBER")
    __verify_token_type("05", "NUMBER")
    __verify_token_type("024", "NUMBER")
    __verify_token_type("298754", "NUMBER")
    __verify_token_type("105", "NUMBER")
    __verify_token_type("76485658457485", "NUMBER")
    __verify_token_type("3286592", "NUMBER")

    __verify_token_type("-1", "NUMBER")
    __verify_token_type("-0", "NUMBER")
    __verify_token_type("-13", "NUMBER")
    __verify_token_type("-835623", "NUMBER")
    __verify_token_type("-65987265795785", "NUMBER")

    __verify_token_type("1.1", "NUMBER")
    __verify_token_type("1.0", "NUMBER")
    __verify_token_type("0.1", "NUMBER")
    __verify_token_type("0.0", "NUMBER")
    __verify_token_type("87.69", "NUMBER")
    __verify_token_type("9832.7745756892246", "NUMBER")
    __verify_token_type("000287650.0002865832000", "NUMBER")

    __verify_token_type("-0.1", "NUMBER")
    __verify_token_type("-0.0", "NUMBER")
    __verify_token_type("-87.69", "NUMBER")
    __verify_token_type("-9832.7745756892246", "NUMBER")
    __verify_token_type("-000287650.0002865832000", "NUMBER")

    __verify_not_token_type("b1", "NUMBER")
    __verify_not_token_type("B1", "NUMBER")
    __verify_not_token_type("1b", "NUMBER")
    __verify_not_token_type("1B", "NUMBER")
    __verify_not_token_type("i6", "NUMBER")
    __verify_not_token_type("l8", "NUMBER")
    __verify_not_token_type("L8", "NUMBER")
    __verify_not_token_type("u3", "NUMBER")
    __verify_not_token_type("U3", "NUMBER")


def test_boolean_literals():
    """Handling boolean literals."""

    __verify_token_type("true", "BOOLEAN")
    __verify_token_type("false", "BOOLEAN")

    __verify_not_token_type("truey", "BOOLEAN")
    __verify_not_token_type("falsey", "BOOLEAN")
    __verify_not_token_type("true9", "BOOLEAN")
    __verify_not_token_type("false5", "BOOLEAN")
