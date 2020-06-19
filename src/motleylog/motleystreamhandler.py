import logging
class MotleyStreamHandler(logging.StreamHandler):
    def __init__(self,stream=None):
        super().__init__(stream)

    def emit(self, record):
        super().emit(record)
        self.flush()
