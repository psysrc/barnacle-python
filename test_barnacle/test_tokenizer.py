"""
test_tokenizer.py: Unit tests for the bcl_tokenizer submodule.
"""

from bcl_tokenizer import tokenizer as tkn


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
