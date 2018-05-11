import logging
import logging.handlers
from ParsingShinken import ParsingShinken

class FailedFilesHandler:
    path_log = "/var/log/shinken/jira/failedFilesHandler.log"
    failed_path_alerts = '/tmp/alerts/f'
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

    def retryFailedFile(self, file_alert, error_conf, step):
        self.logger.warning('*****File' + file_alert+ 'has failed on its: '+step + ' step with error message '+ error_conf+'*****')
        self.logger.warning('Attempting retry of failed file.')
        parsing = ParsingShinken()

        parsed=false
        for i in (0,2) and parsed==false:
            myparsingdata, error = parsing.parsingfiles(self.path_alerts, file_alert)
            if error:
                self.logger.warning('Attempt '+(i+1) +'of '+step +' step for file ' + str(file_alert[1])  +'has failed')
                self.logger.warning('Error message:'+ error)

                if i==2 and error:
                    self.logger.warning('Moving file to  ' + failed_path_alerts + 'has file cannot be parsed.')
                    os.rename(path_alerts + '/' + str(file_alert[1]), failed_path_alerts + '/' + str(file_alert[1]))
            else:
                parsed=true




