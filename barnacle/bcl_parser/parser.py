"""
Implements the Parser class.
"""

from typing import Callable, List

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

        if self.token_lookahead["type"] != expected_token:
            actual_token_type = self.token_lookahead["type"]
            raise SyntaxError(f"Unexpected token (expected '{expected_token}', got '{actual_token_type}')")

        token = self.token_lookahead
        self.token_lookahead = self.tokenizer.next_token()
        return token

    def __node_program(self) -> dict:
        """
        Program node: Represents a Barnacle program.

        A program node consists of zero or more `statement` nodes.
        """

        statements = []

        while self.token_lookahead["type"] != "PROGRAM_END":
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
        -   a `while` node
        -   a `do_while` node
        -   a `return` node
        -   a `func_call` node
        """

        branches = {
            "PRINT": self.__node_print,
            "LET": self.__node_var_declaration,
            "FUNC": self.__node_func_declaration,
            "IF": self.__node_conditional,
            "IDENTIFIER": self.__ambiguous_node_var_assignment_or_func_call,
            "{": self.__node_code_block,
            "WHILE": self.__node_while_loop,
            "DO": self.__node_do_while_loop,
            "RETURN": self.__node_return,
        }

        return self.__construct_multibranch_node("statement", branches)

    def __node_do_while_loop(self) -> dict:
        """
        Do While loop node: Represents a 'do-while' loop.

        A do-while loop consists of the 'DO' token, a code block, a 'WHILE' token and an expression.
        """

        self.__consume_token("DO")
        body = self.__node_code_block()
        self.__consume_token("WHILE")
        expression = self.__node_expression()

        return {
            "type": "do_while",
            "expression": expression,
            "body": body,
        }

    def __ambiguous_node_var_assignment_or_func_call(self) -> dict:
        """
        An ambiguous node which is either a variable assignment or a function call.
        Both nodes begin with an `IDENTIFIER` token.
        """

        identifier = self.__node_identifier()

        if self.token_lookahead["type"] == "=":
            return self.__node_var_assignment(identifier)

        return self.__node_func_call(identifier)

    def __node_func_call(self, identifier: dict | None = None) -> dict:
        """
        Represents a function call.

        A function call consists of the token stream `identifier ( ... )`,
        where `(` and `)` are tokens, `identifier` is a node,
        and `...` consists of 0 or more `identifier` nodes separated by `,` tokens.
        """

        if identifier is None:
            identifier = self.__node_identifier()

        self.__consume_token("(")

        parameters = []
        if self.token_lookahead["type"] != ")":
            parameters.append(self.__node_expression())

            while self.token_lookahead["type"] == ",":
                self.__consume_token(",")
                parameters.append(self.__node_expression())

        self.__consume_token(")")

        return {
            "type": "func_call",
            "identifier": identifier,
            "parameters": parameters,
        }

    def __node_return(self) -> dict:
        """
        Return node: Represents a 'return' statement within a function code block.

        A return statement consists of the token stream `RETURN expression`,
        where `RETURN` is a RETURN token, and `expression` is an expression node.
        """

        self.__consume_token("RETURN")
        expression = self.__node_expression()

        return {
            "type": "return",
            "body": expression,
        }

    def __node_while_loop(self) -> dict:
        """
        While loop node: Represents a 'while' loop.

        A while loop consists of the 'WHILE' token, an expression, and a code block.
        """

        self.__consume_token("WHILE")
        expression = self.__node_expression()
        body = self.__node_code_block()

        return {
            "type": "while",
            "expression": expression,
            "body": body,
        }

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

    def __node_var_assignment(self, identifier: dict | None = None) -> dict:
        """
        Variable Assignment node: Represents a variable assignment.

        A variable assignment consists of the stream `identifier = expression`,
        where `identifier` and `expression` are nodes.
        """

        if identifier is None:
            identifier = self.__node_identifier()

        self.__consume_token("=")
        expression = self.__node_expression()

        return {
            "type": "var_assignment",
            "identifier": identifier,
            "value": expression,
        }

    def __node_expression(self) -> dict:
        """Expression node: Represents an expression whose value can be calculated."""

        return self.__node_low_precedence_operator_expression()

    def __node_parenthesised_expression(self) -> dict:
        """Represents an expression within parentheses."""

        self.__consume_token("(")
        expression = self.__node_expression()
        self.__consume_token(")")

        return expression

    def __node_primary_expression(self) -> dict:
        """Represents the highest-possible precedence expression, either a value or a parenthesised expression."""

        if self.token_lookahead["type"] == "(":
            return self.__node_parenthesised_expression()

        return self.__node_value()

    def __node_value(self) -> dict:
        """Represents a single value, either a literal or variable of indeterminate type."""

        branches = {
            "STRING": self.__node_string_literal,
            "NUMBER": self.__node_numeric_literal,
            "BOOLEAN": self.__node_boolean_literal,
            "IDENTIFIER": self.__ambiguous_node_identifier_or_func_call,
        }

        return self.__construct_multibranch_node("value", branches)

    def __ambiguous_node_identifier_or_func_call(self) -> dict:
        """
        An ambiguous node which is either an identifier or a function call.
        Both nodes begin with an `IDENTIFIER` token.
        """

        identifier = self.__node_identifier()

        if self.token_lookahead["type"] == "(":
            return self.__node_func_call(identifier)

        return identifier

    def __node_binary_expression(self, operator_tokens: List[str], sub_expression_parser: Callable) -> dict:
        """
        Represents a left-associative expression with the given operator tokens and a sub-expression parser.

        Left-associative means e.g. `1 + 2 + 3` is calculated as `(1 + 2) + 3`.
        """

        this_expression = sub_expression_parser()

        while self.token_lookahead["type"] in operator_tokens:
            operator = self.__consume_token(self.token_lookahead["type"])["value"]

            right_operand = sub_expression_parser()

            this_expression = {
                "type": "binary_expression",
                "operator": operator,
                "left": this_expression,
                "right": right_operand,
            }

        return this_expression

    def __node_low_precedence_operator_expression(self) -> dict:
        """Represents an expression to be calculated containing low-precedence operators."""

        operator_tokens = ["+", "-", "==", "!="]
        return self.__node_binary_expression(operator_tokens, self.__node_medium_precedence_operator_expression)

    def __node_medium_precedence_operator_expression(self) -> dict:
        """Represents an expression to be calculated containing medium-precedence operators."""

        operator_tokens = ["*", "/", "<", "<=", ">", ">="]
        return self.__node_binary_expression(operator_tokens, self.__node_high_precedence_operator_expression)

    def __node_high_precedence_operator_expression(self) -> dict:
        """Represents an expression to be calculated containing high-precedence operators."""

        operator_tokens = []
        return self.__node_binary_expression(operator_tokens, self.__node_primary_expression)

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
        if self.token_lookahead["type"] == "ELSE":
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
