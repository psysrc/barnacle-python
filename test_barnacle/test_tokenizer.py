from bcl_tokenizer import tokenizer as tkn


def test_empty():
    tokenizer = tkn.Tokenizer("")
    assert not tokenizer.has_more_tokens()
    assert tokenizer.next_token() is None
