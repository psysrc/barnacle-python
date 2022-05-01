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
        self.variables = dict()

    def new_variable(self, identifier, value):
        logging.debug(f"Adding variable '{identifier}' to environment")
        if identifier in self.variables:
            raise RuntimeError(f"Tried to declare variable '{identifier}' which already exists")

        self.variables[identifier] = value

    def update_variable(self, identifier, value):
        logging.debug(f"Updating variable '{identifier}' in environment")
        if identifier not in self.variables:
            raise RuntimeError(f"Tried to update variable '{identifier}' which has not been declared")

        self.variables[identifier] = value

    def remove_variable(self, identifier):
        logging.debug(f"Removing variable '{identifier}' from environment")
        if identifier not in self.variables:
            raise RuntimeError(f"Tried to remove variable '{identifier}' which has not been declared")

        self.variables.pop(identifier)
