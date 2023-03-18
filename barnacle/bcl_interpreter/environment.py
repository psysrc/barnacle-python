"""
Implements the Environment class.
"""

import logging

from bcl_interpreter.function import Function


class Environment:
    """
    A Barnacle environment which can hold variables and function definitions.
    """

    def __init__(self, outer_environment=None):
        logging.debug("New environment created")

        self.__parent: Environment = outer_environment
        self.__variables: dict = {}
        self.__functions: list[Function] = []

    def new_variable(self, identifier, value):
        """
        Define a new variable in this environment.

        If the variable already exists, a RuntimeError is raised.
        """

        logging.debug("Adding variable '%s' to environment", identifier)

        if identifier in self.__variables:
            raise RuntimeError(f"Tried to declare variable '{identifier}' which already exists")

        self.__variables[identifier] = value

    def update_variable(self, identifier, value):
        """
        Update an existing variable in this environment or the outer environment.

        If the variable does not exist, a RuntimeError is raised.
        """

        logging.debug("Updating variable '%s' in environment", identifier)

        if identifier in self.__variables:
            self.__variables[identifier] = value
        elif self.__parent is not None:
            self.__parent.update_variable(identifier, value)
        else:
            raise RuntimeError(f"Tried to update variable '{identifier}' which has not been declared")

    def remove_variable(self, identifier):
        """
        Delete an existing variable in this environment.

        If the variable does not exist, a RuntimeError is raised.
        """

        logging.debug("Removing variable '%s' from environment", identifier)

        if identifier not in self.__variables:
            raise RuntimeError(f"Tried to remove variable '{identifier}' which has not been declared")

        self.__variables.pop(identifier)

    def get_variable(self, identifier):
        """
        Fetches the value of an existing variable in this environment or the parent environment.

        If the variable does not exist, a RuntimeError is raised.
        """

        logging.debug("Getting variable '%s' from environment", identifier)

        if identifier in self.__variables:
            return self.__variables[identifier]

        if self.__parent is not None:
            return self.__parent.get_variable(identifier)

        raise RuntimeError(f"Tried to get variable '{identifier}' which has not been declared")

    def new_function(self, identifier: str, parameters: list[str], code_block: dict):
        """
        Define a new function in this environment.

        If the function name already exists, a RuntimeError is raised.
        """

        logging.debug("Adding function '%s' to environment", identifier)

        if identifier in self.__functions:
            raise RuntimeError(f"Tried to declare function '{identifier}' which already exists")

        self.__functions.append(Function(name=identifier, parameters=parameters, code_block=code_block))
