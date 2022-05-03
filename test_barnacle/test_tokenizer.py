from bcl_tokenizer import tokenizer as tkn


def test_empty():
    tokenizer = tkn.Tokenizer("")
    assert not tokenizer.has_more_tokens()
    assert tokenizer.next_token() is None

def test_whitespace_only():
    source = "         \n      \n\n\t\n \n \r\n \r      \r\n\r \t     \t \t\r\t\rn"
    tokenizer = tkn.Tokenizer(source)

    assert not tokenizer.has_more_tokens()
    assert tokenizer.next_token() is None
