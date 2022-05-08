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
        """
        Parse the source and return the AST.

        If parsing fails at any point, a SyntaxError will be raised.
        """

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
        surrounded by `{` and `}` tokens.
        """

        self.__consume_token("{")

        statements = []

        while self.token_lookahead["type"] != "}":
            statements.append(self.__node_statement())

        self.__consume_token("}")

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
        -   a `func_declaration` node
        -   a `conditional` node
        -   a `var_assignment` node
        -   a `code_block` node
        """

        branches = {
            "PRINT": self.__node_print,
            "LET": self.__node_var_declaration,
            "FUNC": self.__node_func_declaration,
            "IF": self.__node_conditional,
            "IDENTIFIER": self.__node_var_assignment,
            "{": self.__node_code_block,
        }

        return self.__construct_multibranch_node("statement", branches)

    def __node_print(self) -> dict:
        """
        Print node: Represents a basic print statement.

        A print statement consists of the token `PRINT` and an `expression` node.
        """

        self.__consume_token("PRINT")
        body = self.__node_expression()

        return {
            "type": "print",
            "body": body,
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
        number = float(number_str) if "." in number_str else int(number_str)

        return {
            "type": "numeric_literal",
            "value": number,
        }

    def __node_boolean_literal(self) -> dict:
        """
        Boolean literal node: Represents a boolean literal.

        A boolean literal consists of the token `BOOLEAN`.
        """

        bool_str = self.__consume_token("BOOLEAN")["value"]
        bool_val = bool_str == "true"

        return {
            "type": "boolean_literal",
            "value": bool_val,
        }

    def __node_identifier(self) -> dict:
        """
        Identifier node: Represents an identifier (e.g. a function name or a variable name).

        An identifier consists of the token stream `IDENTIFIER`.
        """

        identifier = self.__consume_token("IDENTIFIER")["value"]

        return {
            "type": "identifier",
            "name": identifier,
        }

    def __node_var_declaration(self) -> dict:
        """
        Variable Declaration node: Represents a variable declaration and assignment.

        A variable declaration consists of the stream `LET identifier = expression`,
        where `LET` and `=` are tokens, and `identifier` and `expression` are nodes.
        """

        self.__consume_token("LET")
        identifier = self.__node_identifier()
        self.__consume_token("=")
        expression = self.__node_expression()

        return {
            "type": "var_declaration",
            "identifier": identifier,
            "value": expression,
        }

    def __node_var_assignment(self) -> dict:
        """
        Variable Assignment node: Represents a variable assignment.

        A variable assignment consists of the stream `identifier = expression`,
        where `identifier` and `expression` are nodes.
        """

        identifier = self.__node_identifier()
        self.__consume_token("=")
        expression = self.__node_expression()

        return {
            "type": "var_assignment",
            "identifier": identifier,
            "value": expression,
        }

    def __node_expression(self) -> dict:
        """
        Expression node: Represents an expression whose value can be calculated.

        An expression can be either:
        -   a `numeric_literal` node
        -   a `string_literal` node
        -   a `boolean_literal` node
        -   an `identifier` node
        """

        branches = {
            "STRING": self.__node_string_literal,
            "NUMBER": self.__node_numeric_literal,
            "BOOLEAN": self.__node_boolean_literal,
            "IDENTIFIER": self.__node_identifier,
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
        Conditional node: Represents an 'if' statement followed by a code block, 0 or more 'else if' statements
        each followed by a code block, and optionally an 'else' statement followed by a code block.

        A conditional node consists of at least the `IF` token, an `expression` node, and a `code_block` node.
        It may be immediately followed by an `ELSE` token, which in turn will be immediately followed by either
        another `conditional` node, or a `code_block` node.
        """

        self.__consume_token("IF")

        expression = self.__node_expression()
        on_true_block = self.__node_code_block()

        on_false_block = None
        if self.token_lookahead is not None and self.token_lookahead["type"] == "ELSE":
            self.__consume_token("ELSE")

            if self.token_lookahead["type"] == "IF":
                on_false_block = self.__node_conditional()
            else:
                on_false_block = self.__node_code_block()

        return {
            "type": "conditional",
            "expression": expression,
            "on_true": on_true_block,
            "on_false": on_false_block,
        }

    def __node_func_declaration(self) -> dict:
        """
        Function Declaration node: Represents a function declaration.

        A function declaration consists of the stream `FUNC identifier ( ... ) code_block`,
        where `FUNC`, `(` and `)` are tokens,
        and `identifier` and `code_block` are nodes,
        and `...` consists of 0 or more `identifier` nodes separated by `,` tokens.
        """

        self.__consume_token("FUNC")

        identifier = self.__node_identifier()

        self.__consume_token("(")

        parameters = []
        if self.token_lookahead["type"] == "IDENTIFIER":
            parameters.append(self.__node_identifier())

            while self.token_lookahead["type"] == ",":
                self.__consume_token(",")
                parameters.append(self.__node_identifier())

        self.__consume_token(")")

        body = self.__node_code_block()

        return {
            "type": "func_declaration",
            "identifier": identifier,
            "parameters": parameters,
            "body": body,
        }
