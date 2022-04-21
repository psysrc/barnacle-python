"""
parser.py: Implements the Parser class.
"""

from bcl_tokenizer import tokenizer as tkn


class Parser:
    """
    The Barnacle Parser.

    Performs syntactic analysis of the tokenized source code to produce an Abstract Syntax Tree (AST).
    The AST can then be interpreted by the Barnacle Interpreter class.
    """
    
    def __init__(self, source):
        self.source = source
        self.tokenizer = tkn.Tokenizer(source)

    def parse(self) -> dict:
        while True:
            token = self.tokenizer.next_token()
            if token is None:
                break

            print(token)
