import datetime
import logging
import os
import sys


class Logger:
    def __init__(self, cmd_level=logging.DEBUG, file_level=logging.DEBUG):
        # Todo: log rotate
        now = datetime.datetime.now()
        log_file = str(now.strftime("%Y-%m-%d")) + ".log"
        if not os.path.exists(log_file):
            open(log_file, "a+", encoding='utf-8')
        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] {%(module)s:%(lineno)d} %(message)s', '%m-%d %H:%M:%S')
        # set cmd log info
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(fmt)
        sh.setLevel(cmd_level)
        # set file log info
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, *message):
        self.logger.debug(message)

    def info(self, *message):
        self.logger.info(message)

    def warning(self, *message):
        self.logger.warning(message)

    def error(self, *message):
        self.logger.error(message)

    def critical(self, *message):
        self.logger.critical(message)

if __name__ == "__main__":
    l = Logger()
    l.info(l.logger.handlers[0])
    a='∠( ᐛ 」∠)＿'
    # a.encode('utf-8').decode('utf-8')
    l.info(a)
