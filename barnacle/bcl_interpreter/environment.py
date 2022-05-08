"""
environment.py: Implements the Environment class.
"""

import logging


class Environment:
    """
    A Barnacle environment which can hold variables and function definitions.
    """

    def __init__(self):
        logging.debug("New environment created")
        self.variables = {}

    def new_variable(self, identifier, value):
        """
        Define a new variable in this environment.

        If the variable already exists, a RuntimeError is raised.
        """

        logging.debug("Adding variable '%s' to environment", identifier)
        if identifier in self.variables:
            raise RuntimeError(f"Tried to declare variable '{identifier}' which already exists")

        self.variables[identifier] = value

    def update_variable(self, identifier, value):
        """
        Update an existing variable in this environment.

        If the variable does not exist, a RuntimeError is raised.
        """

        logging.debug("Updating variable '%s' in environment", identifier)
        if identifier not in self.variables:
            raise RuntimeError(f"Tried to update variable '{identifier}' which has not been declared")

        self.variables[identifier] = value

    def remove_variable(self, identifier):
        """
        Delete an existing variable in this environment.

        If the variable does not exist, a RuntimeError is raised.
        """

        logging.debug("Removing variable '%s' from environment", identifier)
        if identifier not in self.variables:
            raise RuntimeError(f"Tried to remove variable '{identifier}' which has not been declared")

        self.variables.pop(identifier)

    def get_variable(self, identifier):
        """
        Fetches the value of an existing variable in this environment.

        If the variable does not exist, a RuntimeError is raised.
        """

        logging.debug("Getting variable '%s' from environment", identifier)
        if identifier not in self.variables:
            raise RuntimeError(f"Tried to get variable '{identifier}' which has not been declared")

        return self.variables[identifier]
