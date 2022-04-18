import logging

from tokenizer import tokenizer as tkn


def run(filename: str):
    """Runs the Barnacle interpreter on the specified file."""

    logging.debug(f"Opening file '{filename}'")

    with open(filename, "r") as script:
        logging.info(f"Running script '{filename}'")
        print(f"+++ BARNACLE RUN '{filename}' +++")

        source = script.read()
        tokenizer = tkn.Tokenizer(source)

        while True:
            token = tokenizer.next_token()
            if token is None:
                break

            print(token)

        print(f"--- BARNACLE END '{filename}' ---")

    logging.info(f"Finished interpreting script")
