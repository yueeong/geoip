import logging

def setup_file_logger(logger_name, log_file, show_in_console=False, level=logging.DEBUG):

    l = logging.getLogger(logger_name)
    l.setLevel(level)

    # Create the handlers
    fileHandler = logging.FileHandler(log_file)
    consolehandler = logging.StreamHandler()

    #config the formatter
    formatter = logging.Formatter('%(asctime)s - {%(module)s} - line[%(lineno)d] : %(message)s')

    #Config the handlers with the formatter and the level to report
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(level=level)

    consolehandler.setFormatter(formatter)
    consolehandler.setLevel(level=level)

    l.addHandler(fileHandler)
    if show_in_console:
        l.addHandler(consolehandler)

    l.info("Logger set up...")