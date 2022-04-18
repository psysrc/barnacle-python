"""
tokenizer.py: Implements the Tokenizer class.

The Tokenizer is responsible for the lexical analysis of the source code.
It will produce a stream of tokens which can then undergo syntactic analysis.
"""

import re
import logging
from . import tokens


class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        logging.debug("Tokenizer initialised")

    def next_token(self) -> dict:
        if not self.has_more_tokens():
            return None

        for regexp, token_type in tokens.TOKEN_REGEXPS.items():
            match = re.search(regexp, self.source)

            if match:
                token_value = match.group()
                self.source = self.source[len(token_value):]

                if token_type:
                    logging.debug(f"Tokenizer matched token '{token_value}' of type '{token_type}'")

                    return {
                        "type":  token_type,
                        "value": token_value,
                    }

                else:
                    return self.next_token()

        raise SyntaxError(f"Unknown syntax near characters '{self.source[:10]}'")

    def has_more_tokens(self) -> bool:
        return bool(self.source)
