import logging
def get_logger(name:str)->logging.Logger:
    logger=logging.getLogger(name) # get the logs by name
    if not logger.handlers: # prevent adding multiple handlers if the logger already has handlers
        h=logging.StreamHandler() # handler to output logs to the console
        formatter=logging.Formatter('[%(asctime)s] - [%(name)s] - [%(message)s]') # formate of the logs
        h.setFormatter(formatter) # set the formatter for the handler
        logger.addHandler(h) # add the handler to the logger
        logger.setLevel(logging.INFO) # set the logging level
    return logger 