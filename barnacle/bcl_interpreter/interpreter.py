"""
Implements the Interpreter class.
"""

import logging

from bcl_interpreter.environment import Environment
from bcl_parser import parser as prs

from .operations import calculate_binary_operation


class Interpreter:
    """
    The Barnacle Interpreter.
    """

    def __init__(self, source: str):
        self.__ast = prs.Parser(source).parse()
        logging.debug("Finished parsing source")

    def run(self):
        """Runs the Barnacle interpreter on the provided source."""

        global_env = Environment()

        self.__interpret_program(global_env, self.__ast)

    def __validate_node_has_type(self, ast: dict):
        """
        Validates that the AST node has a `type` key.
        """

        if "type" not in ast.keys():
            logging.debug("Node has no 'type' key: %s", ast)
            raise RuntimeError("Node has no 'type' key")

    def __validate_node(self, ast: dict, expected_type: str, expected_keys: set):
        """
        Validates that the AST node has the expected type and contains the expected keys.

        An AST node should always have a `type` key, so this does not need to be provided when calling this function.
        """

        self.__validate_node_has_type(ast)

        expected_keys.add("type")

        if ast["type"] != expected_type:
            actual_type = ast["type"]
            logging.debug("Node has unexpected type: %s", ast)
            raise RuntimeError(f"Node has unexpected type (expected '{expected_type}', got '{actual_type}')")

        if set(ast.keys()) != expected_keys:
            logging.debug("Node does not contain the expected keys: %s", ast)
            raise RuntimeError(
                f"Node does not contain the expected keys (expected '{expected_keys}', got '{set(ast.keys())}')"
            )

    def __interpret_program(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'program' node")
        self.__validate_node(ast, "program", {"body"})

        for statement in ast["body"]:
            self.__interpret_statement(env, statement)

    def __interpret_statement(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'statement' node")

        branches = {
            "print": self.__interpret_print,
            "conditional": self.__interpret_conditional,
            "var_declaration": self.__interpret_var_declaration,
            "var_assignment": self.__interpret_var_assignment,
            "code_block": self.__interpret_code_block,
            "while": self.__interpret_while_loop,
            "func_declaration": self.__interpret_func_declaration,
            "func_call": self.__interpret_func_call,
        }

        self.__construct_multibranch_interpret(env, ast, "statement", branches)

    def __interpret_func_call(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'func_call' node")
        self.__validate_node(ast, "func_call", {"identifier", "parameters"})

        identifier = self.__interpret_identifier_node(env, ast["identifier"])
        function, declaring_env = env.get_function(identifier)

        declared_params = function.parameters
        provided_params = ast["parameters"]

        if len(provided_params) != len(declared_params):
            raise RuntimeError(
                f"Tried to call function {identifier} with incorrect number of parameters"
                f"(expected {len(declared_params)}, got {len(provided_params)})"
            )

        provided_params = [self.__interpret_expression(env, param) for param in provided_params]

        func_env = Environment(outer_environment=declaring_env)

        parameter_pairs = zip(declared_params, provided_params)
        for param_name, param_value in parameter_pairs:
            func_env.new_variable(param_name, param_value)

        self.__interpret_code_block(func_env, function.code_block)

    def __interpret_func_declaration(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'func_declaration' node")
        self.__validate_node(ast, "func_declaration", {"identifier", "parameters", "body"})

        identifier = self.__interpret_identifier_node(env, ast["identifier"])
        parameters = [self.__interpret_identifier_node(env, param_ast) for param_ast in ast["parameters"]]
        code_block = ast["body"]

        env.new_function(identifier, parameters, code_block)

    def __interpret_print(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'print' node")
        self.__validate_node(ast, "print", {"body"})

        expression = self.__interpret_expression(env, ast["body"])

        if isinstance(expression, bool):
            expression = "true" if expression else "false"

        print(expression)

    def __interpret_string_literal(self, _: Environment, ast: dict):
        logging.debug("Interpreting 'string_literal' node")
        self.__validate_node(ast, "string_literal", {"value"})

        return ast["value"]

    def __interpret_numeric_literal(self, _: Environment, ast: dict):
        logging.debug("Interpreting 'numeric_literal' node")
        self.__validate_node(ast, "numeric_literal", {"value"})

        return ast["value"]

    def __interpret_boolean_literal(self, _: Environment, ast: dict):
        logging.debug("Interpreting 'boolean_literal' node")
        self.__validate_node(ast, "boolean_literal", {"value"})

        return ast["value"]

    def __interpret_expression(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'expression' node")

        branches = {
            "string_literal": self.__interpret_string_literal,
            "numeric_literal": self.__interpret_numeric_literal,
            "boolean_literal": self.__interpret_boolean_literal,
            "identifier": self.__interpret_variable,
            "binary_expression": self.__interpret_binary_expression,
        }

        return self.__construct_multibranch_interpret(env, ast, "expression", branches)

    def __interpret_binary_expression(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'binary_expression' node")
        self.__validate_node(ast, "binary_expression", {"left", "right", "operator"})

        left_value = self.__interpret_expression(env, ast["left"])
        right_value = self.__interpret_expression(env, ast["right"])
        operator = ast["operator"]

        result = calculate_binary_operation(operator=operator, left=left_value, right=right_value)
        return result

    def __construct_multibranch_interpret(self, env: Environment, ast: dict, interpret_name: str, branches: dict):
        self.__validate_node_has_type(ast)

        node_type = ast["type"]

        if node_type in branches:
            return branches[node_type](env, ast)

        logging.debug("Unexpected node type while interpreting '%s' node: %s", interpret_name, ast)
        raise RuntimeError(f"Unexpected node type '{node_type}' while interpreting '{interpret_name}'")

    def __interpret_conditional(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'conditional' node")
        self.__validate_node(ast, "conditional", {"expression", "on_true", "on_false"})

        expression = self.__interpret_expression(env, ast["expression"])

        if bool(expression):
            logging.debug("Interpreting conditional 'on_true' node")
            self.__interpret_code_block(env, ast["on_true"])
        elif (on_false_ast := ast["on_false"]) is not None:
            logging.debug("Interpreting conditional 'on_false' node")
            self.__validate_node_has_type(on_false_ast)

            if on_false_ast["type"] == "conditional":
                self.__interpret_conditional(env, on_false_ast)
            else:
                self.__interpret_code_block(env, on_false_ast)

    def __interpret_code_block(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'code_block' node")
        self.__validate_node(ast, "code_block", {"body"})

        new_env = Environment(env)

        for statement in ast["body"]:
            self.__interpret_statement(new_env, statement)

    def __interpret_var_declaration(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'var_declaration' node")
        self.__validate_node(ast, "var_declaration", {"identifier", "value"})

        variable_name = self.__interpret_identifier_node(env, ast["identifier"])
        variable_value = self.__interpret_expression(env, ast["value"])

        env.new_variable(variable_name, variable_value)

    def __interpret_var_assignment(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'var_assignment' node")
        self.__validate_node(ast, "var_assignment", {"identifier", "value"})

        variable_name = self.__interpret_identifier_node(env, ast["identifier"])
        variable_value = self.__interpret_expression(env, ast["value"])

        env.update_variable(variable_name, variable_value)

    def __interpret_identifier_node(self, _: Environment, ast: dict):
        logging.debug("Interpreting 'identifier' node")
        self.__validate_node(ast, "identifier", {"name"})

        return ast["name"]

    def __interpret_variable(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'variable' node")

        variable_name = self.__interpret_identifier_node(env, ast)

        return env.get_variable(variable_name)

    def __interpret_while_loop(self, env: Environment, ast: dict):
        logging.debug("Interpreting 'while' node")
        self.__validate_node(ast, "while", {"expression", "body"})

        conditional_value = self.__interpret_expression(env, ast["expression"])

        while conditional_value:
            self.__interpret_code_block(env, ast["body"])
            conditional_value = self.__interpret_expression(env, ast["expression"])
