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

        if self.token_lookahead["type"] != expected_token:
            actual_token_type = self.token_lookahead["type"]
            raise RuntimeError(f"Unexpected token (expected '{expected_token}', got '{actual_token_type}')")

        token = self.token_lookahead
        self.token_lookahead = self.tokenizer.next_token()
        return token

    def __node_program(self) -> dict:
        """
        Program node: Represents a Barnacle program.

        A program node consists of zero or more `statement` nodes.
        """

        statements = []

        while self.token_lookahead is not None:
            statements.append(self.__node_statement())

        return {
            "type": "program",
            "body": statements,
        }

    def __node_code_block(self) -> dict:
        """
        Code Block node: Represents a block of code.

        A code block node consists of zero or more `statement` nodes,
        surrounded by `START_CODE_BLOCK` and `END_CODE_BLOCK` tokens.
        """

        self.__consume_token("START_CODE_BLOCK")

        statements = []

        while self.token_lookahead["type"] != "END_CODE_BLOCK":
            statements.append(self.__node_statement())

        self.__consume_token("END_CODE_BLOCK")

        return {
            "type": "code_block",
            "body": statements,
        }

    def __node_statement(self) -> dict:
        """
        Statement node: Represents a single executable statement.

        A statement can be one of:
        -   a `print` node
        -   a `var_declaration` node
        -   a `conditional` node
        """

        branches = {
            "PRINT": self.__node_print,
            "LET": self.__node_var_declaration,
            "IF": self.__node_conditional,
        }

        return self.__construct_multibranch_node("statement", branches)

    def __node_print(self) -> dict:
        """
        Print node: Represents a basic print statement.

        A print statement consists of the token `PRINT` and a `string_literal` node.
        """

        self.__consume_token("PRINT")
        string_literal = self.__node_string_literal()

        return {
            "type": "print",
            "body": string_literal,
        }

    def __node_string_literal(self) -> dict:
        """
        String literal node: Represents a string literal.

        A string literal consists of the token `STRING`.
        """

        string = self.__consume_token("STRING")["value"]

        return {
            "type": "string_literal",
            "value": string[1:-1],  # Strip start and end quote characters
        }

    def __node_numeric_literal(self) -> dict:
        """
        Numeric literal node: Represents a numeric literal.

        A numeric literal consists of the token `NUMBER`.
        """

        number_str = self.__consume_token("NUMBER")["value"]

        if "." in number_str:
            number = float(number_str)
        else:
            number = int(number_str)

        return {
            "type": "numeric_literal",
            "value": number,
        }

    def __node_var_declaration(self) -> dict:
        """
        Variable Declaration node: Represents a variable declaration and assignment.

        A variable declaration consists of the token stream `LET IDENTIFIER ASSIGN_OP` and an `expression` node.
        """

        self.__consume_token("LET")
        identifier = self.__consume_token("IDENTIFIER")["value"]
        self.__consume_token("ASSIGN_OP")
        expression = self.__node_expression()

        return {
            "type": "var_declaration",
            "identifier": identifier,
            "value": expression,
        }

    def __node_expression(self) -> dict:
        """
        Expression node: Represents an expression whose value can be calculated.

        An expression can be either:
        -   a `numeric_literal` node
        -   a `string_literal` node
        """

        branches = {
            "STRING": self.__node_string_literal,
            "NUMBER": self.__node_numeric_literal,
        }

        return self.__construct_multibranch_node("expression", branches)

    def __construct_multibranch_node(self, node_name: str, branches: dict) -> dict:
        """
        Constructs a multi-branch node.

        If a node has two or more possible forms based on the lookahead token,
        this method can help to construct its behaviour.

        Parameters
        ----------
        `node_name` should be the name of the node being constructed.

        `branches` should be a dictionary where the keys are token types and the value is a node function.
        """

        lookahead_type = self.token_lookahead["type"]

        if lookahead_type in branches:
            return branches[lookahead_type]()

        raise SyntaxError(f"Unexpected token '{lookahead_type}' while parsing '{node_name}' node")

    def __node_conditional(self) -> dict:
        """
        Conditional node: Represents an 'if' statement followed by a code block.

        A conditional node consists of at least the `IF` token, an expression node, and a code block node.
        """

        self.__consume_token("IF")

        return {
            "type": "conditional",
            "expression": self.__node_expression(),
            "on_true": self.__node_code_block(),
        }
