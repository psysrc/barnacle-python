"""
test_tokenizer.py: Unit tests for the bcl_tokenizer submodule.
"""

from bcl_tokenizer import tokenizer as tkn


def __verify_token(source: str, expected_token_type: str):
    """Verify that the source produces exactly one token which has the expected token type when tokenized."""

    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.end_of_stream()

    actual_token = tokenizer.next_token()

    assert actual_token == {"type": expected_token_type, "value": source}

    assert tokenizer.end_of_stream()
    assert tokenizer.next_token() is None


def test_empty():
    """Handling an empty source string."""

    tokenizer = tkn.Tokenizer("")

    assert tokenizer.end_of_stream()
    assert tokenizer.next_token() is None


def test_whitespace():
    """Handling source that is only whitespace."""

    source = "         \n      \n\n\t\n \n \r\n \r      \r\n\r \t     \t \t\r\t\r\n"
    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.end_of_stream()

    assert tokenizer.next_token() is None

    assert tokenizer.end_of_stream()


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

    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.end_of_stream()

    assert tokenizer.next_token() is None

    assert tokenizer.end_of_stream()


def test_number_literals():
    """Handling number literals."""

    __verify_token("0", "NUMBER")
    __verify_token("1", "NUMBER")
    __verify_token("6", "NUMBER")
    __verify_token("10", "NUMBER")
    __verify_token("11", "NUMBER")
    __verify_token("00", "NUMBER")
    __verify_token("00000", "NUMBER")
    __verify_token("05", "NUMBER")
    __verify_token("024", "NUMBER")
    __verify_token("298754", "NUMBER")
    __verify_token("105", "NUMBER")
    __verify_token("76485658457485", "NUMBER")
    __verify_token("3286592", "NUMBER")

    __verify_token("-1", "NUMBER")
    __verify_token("-0", "NUMBER")
    __verify_token("-13", "NUMBER")
    __verify_token("-835623", "NUMBER")
    __verify_token("-65987265795785", "NUMBER")

    __verify_token("1.1", "NUMBER")
    __verify_token("1.0", "NUMBER")
    __verify_token("0.1", "NUMBER")
    __verify_token("0.0", "NUMBER")
    __verify_token("87.69", "NUMBER")
    __verify_token("9832.7745756892246", "NUMBER")
    __verify_token("000287650.0002865832000", "NUMBER")

    __verify_token("-0.1", "NUMBER")
    __verify_token("-0.0", "NUMBER")
    __verify_token("-87.69", "NUMBER")
    __verify_token("-9832.7745756892246", "NUMBER")
    __verify_token("-000287650.0002865832000", "NUMBER")
