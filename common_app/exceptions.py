class ProcessingFailedException(Exception):
    def __init__(self, message, httpStatus=None):
        super().__init__(message)
        self.message = message
        self.httpStatus = httpStatus

    def getMessage(self):
        return self.message
