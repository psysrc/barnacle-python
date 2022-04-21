"""
parser.py: Implements the Parser class.
"""

import string
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
        """
        Program node: Represents a Barnacle program.

        A program consists of zero or more `statement` nodes.
        """

        statements = []

        while self.token_lookahead is not None:
            statements.append(self.__node_statement())

        return {
            "type": "program",
            "statements": statements,
        }

    def __node_statement(self) -> dict:
        """
        Statement node: Represents a single executable statement.

        A statement can be one of:
        -   a `print` node
        """

        return self.__node_print()

    def __node_print(self) -> dict:
        """
        Print node: Represents a basic print statement.

        A print statement consists of the token stream `PRINT STRING`.
        """

        self.__consume_token("PRINT")
        string_literal = self.__node_string_literal()

        return {
            "type": "print",
            "body": string_literal,
        }

    def __node_string_literal(self) -> dict:
        string = self.__consume_token("STRING")["value"]

        return {
            "type": "string_literal",
            "value": string[1:-1],  # Strip start and end quote characters
        }
    
    def __node_numeric_literal(self) -> dict:
        number_str = self.__consume_token("NUMBER")["value"]

        if "." in number_str:
            number = float(number_str)
        else:
            number = int(number_str)

        return {
            "type": "numeric_literal",
            "value": number,
        }
