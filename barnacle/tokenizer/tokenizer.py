class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.tmp = 5

    def next_token(self):
        self.tmp -= 1

        return "Example token" if self.tmp > 0 else None
