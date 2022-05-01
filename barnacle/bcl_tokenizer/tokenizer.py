"""
tokenizer.py: Implements the Tokenizer class.
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

    def next_token(self) -> dict:
        """
        Find and return the next token in the source stream.

        When the end of the stream is reached, None is returned.

        If no token can be found, a SyntaxError is raised.
        """

        if not self.has_more_tokens():
            return None

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

                return self.next_token()

        raise SyntaxError(f"Unknown syntax near characters '{self.source[:10]}'")

    def has_more_tokens(self) -> bool:
        """Returns whether there are any more tokens in the source stream."""

        return bool(self.source)
