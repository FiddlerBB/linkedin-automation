import logging


class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Logger._initialized:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)
             # Clear existing handlers to avoid duplicates
            if self.logger.handlers:
                self.logger.handlers.clear()

            # Create handlers
            c_handler = logging.StreamHandler()
            f_handler = logging.FileHandler("file.log")


            # Set level of handlers
            c_handler.setLevel(logging.INFO)
            f_handler.setLevel(logging.ERROR)

            # Create formatters and add it to handlers
            c_format = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            f_format = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            self.logger.addHandler(c_handler)
            self.logger.addHandler(f_handler)

            Logger._initialized = True

    def debug(self, message: str):
        self.logger.debug(message)
    def info(self, message: str):
        self.logger.info(message)
    def warning(self, message: str):
        self.logger.warning(message)
    def error(self, message: str):
        self.logger.error(message)
    def critical(self, message: str):
        self.logger.critical(message)
