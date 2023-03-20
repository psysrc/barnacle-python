"""
Implements the Tokenizer class.
"""

import logging
import re

from . import tokens


class Tokenizer:
    """
    The Barnacle Tokenizer.

    Performs lexical analysis of the source code to produce a stream of tokens.
    The tokens can then be parsed by the Barnacle Parser class.
    """

    def __init__(self, source: str):
        self.source = source
        logging.debug("Tokenizer initialised")

        self.current_token = self.__get_next_token_from_stream()

    def next_token(self) -> dict:
        """
        Return the next token in the source stream.

        If `end_of_stream() == True`, a sentinel `PROGRAM_END` token is returned.

        If no valid token can be found, a SyntaxError is raised.
        """

        token_to_return = self.current_token

        self.current_token = self.__get_next_token_from_stream()

        return token_to_return

    def __get_next_token_from_stream(self) -> dict:

        if self.__source_is_empty():
            return {
                "type": "PROGRAM_END",
                "value": None,
            }

        for regexp, token_type in tokens.TOKEN_REGEXPS.items():
            match = re.search(regexp, self.source)

            if match:
                token_value = match.group()
                self.source = self.source[len(token_value) :]

                if token_type:
                    logging.debug("Tokenizer matched token '%s' of type '%s'", token_value, token_type)

                    return {
                        "type": token_type,
                        "value": token_value,
                    }

                return self.__get_next_token_from_stream()

        raise SyntaxError(f"Unknown syntax near characters '{self.source[:10]}'")

    def end_of_stream(self) -> bool:
        """Returns whether the end of the stream has been reached."""

        return self.current_token["type"] == "PROGRAM_END"

    def __source_is_empty(self) -> bool:
        return not bool(self.source)
