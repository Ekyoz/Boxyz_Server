import logging

'''
Format args:

File name : %(filename)s
Time : %(asctime)s
Level name : %(levelname)s
Message : %(message)s
Name : %(name)s
Process : %(process)d
Thread name : %(threadName)s
'''

class Logger():

    formatter_log = None
    handler_log = None
    log = None

    def setFormat(self, format : str):
        self.formatter_log = logging.Formatter(format)
    
    def setHandler(self, files : str, mode : str, encoding : str):
        self.handler_log = logging.FileHandler(files, mode=mode, encoding=encoding)
        if(self.formatter_log != None):
            self.handler_log.setFormatter(self.formatter_log)
        if(self.formatter_log == None):
            self.handler_log.setFormatter("%(levelname)s -- %(name)s -- %(message)s")

    def createLog(self, name : str, level : logging):
        self.log = logging.getLogger(name)
        self.log.setLevel(level)
        self.log.addHandler(self.handler_log)

    def debugLog(self, message):
        self.log.debug(message)

    def infoLog(self, message):
        self.log.info(message)

    def warningLog(self, message):
        self.log.warning(message)
    
    def errorLog(self, message):
        self.log.error(message)

    def criticalLog(self, message):
        self.log.critical(message)