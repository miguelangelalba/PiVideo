import logging


def logsFormat(name,path,logName):
    #,datefmt='%d-%b-%y %H:%M:%S'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    fileHandler = logging.FileHandler(path + logName)
    fileHandler.setFormatter(formatter)
    
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    return logger