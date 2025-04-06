import logging

# Set up logging to file
logging.basicConfig(
    filename="scrape.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def logger(message, level="info"):
    """Logs messages with different levels to a file and prints them."""
    level = level.lower()
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "debug":
        logging.debug(message)
    else:
        logging.info(message)  # Default fallback

    print(message)  # Still print to console
