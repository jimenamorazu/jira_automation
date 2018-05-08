import os
import logging
import logging.handlers

class DeleteFilesFromQ:
    jira_path= '..'
    config_value=0
    path_log = "/var/log/shinken/jira/file_removal_log.log"

    logger = logging.getLogger('FileRemoval')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(filename=path_log, mode='a', maxBytes=2000000, backupCount=10)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    def __init__(self,path, config_value):
        self.jira_path=path
        self.config_value=config_value


    def removeFiles(self):
        self.logger.warning('****Checking for files on ' + path_log + 'before JiraAutomation begins**** ')

        if self.config_value=='0':

	    self.logger.info('ConfigFile is set to Maintenance mode. Files waiting for pickup from Shinken will be removed')
            self.logger.info('Deleting files from '+self.jira_path )
            for the_file in os.listdir(self.jira_path):

                self.logger.info('Deleting files from ' + self.jira_path)
                file_path = os.path.join(self.jira_path, the_file)
                try:

                    # if os.path.isfile(file_path):
                    # os.unlink(file_path)
                    self.logger.info('Deleting file ' + file_path)

                except Exception:
                    self.logger.critical('An unexpected error occurred to delete files from /tmp/alerts/q', Exception )

        else:
            self.logger.info('ConfigFile is set to Production/Test mode. Leaving files for pickup by Jira Automation')




