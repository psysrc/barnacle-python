from bcl_tokenizer import tokenizer as tkn


def test_empty():
    tokenizer = tkn.Tokenizer("")

    assert tokenizer.end_of_stream()
    assert tokenizer.next_token() is None


def test_whitespace_only():
    source = "         \n      \n\n\t\n \n \r\n \r      \r\n\r \t     \t \t\r\t\r\n"
    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.end_of_stream()

    assert tokenizer.next_token() is None

    assert tokenizer.end_of_stream()
