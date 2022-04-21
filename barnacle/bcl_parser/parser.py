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

        self.token_lookahead = self.tokenizer.next_token()

    def parse(self) -> dict:
        return self.__node_program()

    def __consume_token(self, expected_token: str) -> dict:
        """
        Consumes the next token in the stream.
        If the token type does not match the provided token_type, an exception is raised.
        """

        if self.token_lookahead is None:
            raise SyntaxError(f"Unexpected end of program, expected '{expected_token}' token")

        # TODO: Un-comment this block; it is important!
        # if self.token_lookahead["type"] != expected_token:
        #     actual_token_type = self.token_lookahead["type"]
        #     raise RuntimeError(f"Unexpected token (expected '{expected_token}', got '{actual_token_type}')")

        token = self.token_lookahead
        self.token_lookahead = self.tokenizer.next_token()
        return token

    def __node_program(self) -> dict:
        statements = []

        while self.token_lookahead is not None:
            statements.append(self.__node_statement())

        return {
            "type": "program",
            "statements": statements,
        }

    def __node_statement(self) -> dict:
        return {
            "type": "statement",
            "body": self.__consume_token(None)["value"]
        }
