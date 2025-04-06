import logging
logging.basicConfig(filename='scrape.log', level=logging.INFO)
def logger(message):
    """Logs messages to a file."""
    logging.info(message)
    print(message)  
