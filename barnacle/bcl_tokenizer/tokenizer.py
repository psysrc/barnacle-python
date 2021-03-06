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

        if self.end_of_stream():
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

    def end_of_stream(self) -> bool:
        """
        Returns whether the end of the stream has been reached.

        If this returns True, `next_token()` will always return None.
        Note that `next_token()` can still return None even if this method returns False.
        """

        return not bool(self.source)
