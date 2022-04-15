import logging


def run(filename: str):
    """Runs the Barnacle interpreter on the specified file."""

    logging.debug(f"Opening file '{filename}'")

    with open(filename, "r") as script:
        logging.info(f"Running script '{filename}'")
        print(f"+++ BARNACLE RUN '{filename}' +++")

        for line in script.readlines():
            print(line)

        print(f"--- BARNACLE END '{filename}' ---")

    logging.info(f"Finished interpreting script")
