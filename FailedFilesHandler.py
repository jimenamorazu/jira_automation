import logging
import logging.handlers
from ParsingShinken import ParsingShinken

class FailedFilesHandler:
    path_log = "/var/log/shinken/jira/failedFilesHandler.log"

    logger = logging.getLogger('FailedFilesHandler')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(filename=path_log, mode='a', maxBytes=2000000, backupCount=10)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    def __init__(self, path_alerts):
        self.path_alerts=path_alerts
        return

    def main(self, file_alert, error_conf):
        self.logger.warning('File has failed while parsing: ' + file_alert+ 'with error message '+error_conf)
        self.logger.warning('Attempting reparse of failed file.')
        parsing = ParsingShinken()

        for i in (0,2):
            myparsingdata, error = parsing.parsingfiles(self.path_alerts, file_alert)
            if error:
                self.logger.warning('Attempt '+(i+1))
