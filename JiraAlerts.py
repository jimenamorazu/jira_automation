#!/usr/bin/python
import logging
import logging.handlers
import os
from ConsumeJiraAPI import ConsumeApi
from DeleteAlertFiles import DeleteAlertFiles
from JiraAlertsConfigFileReader import JiraAlertsConfigFileReader
from JiraMultipleTicket import MultipleJiraTicket
from JiraOneDescriptiontProcess import JiraOneDescriptionProcess
from JiraResponseHandler import JiraResponseHandler
from ParsingShinken import ParsingShinken
from ParsingToJson import ParsingToJson
from DeleteFilesFromQ import DeleteFilesFromQ

class JiraAlerts:
        config = JiraAlertsConfigFileReader()
        path_log = "/var/log/shinken/jira/jiralog.log"
        logger = logging.getLogger('Jira')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(filename=path_log, mode='a', maxBytes=2000000,
                                           backupCount=10)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                          datefmt='%y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        def __init__(self):
                return

        def main(self, valueconf):
                path_alerts = '/tmp/alerts/q'
                myparsingdata = []
                mycol = []
                details = []

                folder = ParsingShinken()
                folder.set_path(path_alerts)

                fileRemover = DeleteFilesFromQ(path_alerts, valueconf)
                fileRemover.removeFiles();

                logger_module = logging.getLogger('Jira')
                logger_module.info('Listing files on alert folder ' + path_alerts)

                files, error_conf = folder.readfolder

                if error_conf:
                        logger_module.critical('Fatal error reading the alert folder' + str(error_conf))
                        logger_module.warning('Jira Automation program terminated')
                        exit(404)
                else:

                        count = len(files)

                        if len(files) > 0:

                                logger_module.info('found ' + str(count) + ' files on folder')
                                logger_module.info('found ' + str(files) + ' on folder')

                                for file_alert in enumerate(files):

                                        del mycol[:]
                                        del details[:]
                                        del myparsingdata[:]

                                        logger_module.info('Parsing process started for ' + str(file_alert[1]) + ' file')

                                        parsing = ParsingShinken()
                                        myparsingdata, error_conf = parsing.parsingfiles(path_alerts, file_alert)

                                        if error_conf:
                                                logger_module.critical('Fatal Error parsing files ' + error_conf)
                                                logger_module.critical('Deleting Alert file, ' + str(file_alert[1]))
                                                deletefile = DeleteAlertFiles()
                                                error_conf = deletefile.deletefile(path_alerts, file_alert)
                                                if (error_conf):
                                                        logger_module.error('Error deleting file, ' + file_alert + ' Error ' + error_conf)
                                                else:
                                                        logger_module.warning('File deleted sucessfully')

                                                logger_module.warning('Jira Automation program terminated')
                                                exit(404)
                                        else:
                                                logger_module.info('Parsing process done for ' + str(file_alert[1]) + ' file')
                                                deletefile = DeleteAlertFiles()
                                                error_conf = deletefile.deletefile(path_alerts, file_alert)
                                                if error_conf:
                                                        logger_module.error('Deleting process failed for ' + str(file_alert))
                                                else:
                                                        logger_module.info('Deleting process successful ' + str(file_alert))



                                        mustprocess, error_conf = self.config.readconfiguration("Host", str(myparsingdata[1])[:-1])
                                        mustprocess = str(mustprocess)

                                        if mustprocess == '0':
                                                logger_module.info(
                                                        'Host set to not process in the configuration file, processing the next host')
                                                delete = DeleteAlertFiles()
                                                error_conf = delete.deletefile(path_alerts, file_alert)

                                                if error_conf:
                                                        logger_module.error('Error deleting alert file ' + file_alert[1] + ' at ' + path_alerts)
                                                        logger_module.error('Error: ' + error_conf)
                                                else:
                                                        exit(1)
                                        else:

                                                mustprocessalert, error_conf = self.config.readconfiguration('AlertsProcessing',
                                                                                                                               str(myparsingdata[4])[:-1])
                                                mustprocessalert = str(mustprocessalert)

                                                if mustprocessalert == '0':
                                                        logger_module.info('Alert  set to not process in the configuration file, processing '
                                                                                           'the next alert')
                                                        delete = DeleteAlertFiles()
                                                        error_conf = delete.deletefile(path_alerts, file_alert)

                                                        if error_conf:
                                                                logger_module.error('Error deleting alert file ' + file_alert[1] + ' at ' + path_alerts)
                                                                logger_module.error('Error: ' + error_conf)
                                                else:

                                                        multithread, error_conf = self.config.readconfiguration('Multithread',
                                                                                                                              str(myparsingdata[4])[:-1])
                                                        multithread = str(multithread)

                                                        if multithread == '0':
                                                                logger_module.info(
                                                                        'Start processing Alert for ' + str(myparsingdata[4][:-1]) + ' on Host ' + str(
                                                                                myparsingdata[1][:-1]) + ' One Jira Mode')
                                                                oneticket = JiraOneDescriptionProcess()
                                                                description = oneticket.processoneticket(myparsingdata)
                                                                tojson = ParsingToJson()
                                                                json = tojson.parsingtojsononetime(description, myparsingdata)
                                                        else:
                                                                logger_module.info(
                                                                        'Start processing Alert for ' + str(myparsingdata[4][:-1]) + ' on Host ' + str(
                                                                                myparsingdata[1][:-1]) + ' Multiple Jira Mode')
                                                                multiple = MultipleJiraTicket()
                                                                mycol, detail, c = multiple.multipleprocesscreation(myparsingdata)
                                                                json = ParsingToJson().parsingtojson(mycol, detail, myparsingdata)

                                                        if valueconf == '1':
                                                                logger_module.info('Test Creating Ticket file successful')
                                                                logger_module.info('Test deleting file successful')

                                                        if valueconf == '2':
                                                                for i in enumerate(json):
                                                                        logger_module.info('Creating Jira ticket Alert ' + '\n' + i[1])
                                                                        consume = ConsumeApi()

                                                                        response, error_conf = consume.callAPI(i[1])
                                                                        responsehandler = JiraResponseHandler()
                                                                        responsehandler.responsehanlder(response, error_conf, str(myparsingdata[4])[:-1])

                                else:
                                        logger_module.info('Alerts no found')
                        else:
                                logger_module.info('Files not found on folder')


if __name__ == '__main__':
        logger_module = logging.getLogger('Jira')
        initializer = JiraAlerts()
        config = JiraAlertsConfigFileReader()

        logger_module.info('*******Reading General configuration for app******')
        module = 'Status'
        option = 'status'
        value, error = config.readconfiguration(str(module), str(option))
        value = str(value)

        path_alerts = '/tmp/alerts/q'
        fileRemover = DeleteFilesFromQ(path_alerts, value)
        fileRemover.removeFiles();

        if error:
                logger_module.error('Error reading configuration file status value')
                logger_module.error('Error, ' + str(error))
                logger_module.error('JiraAlert program terminated')
                exit(404)
        else:
                if value == '0':
                        logger_module.warning('System set to running on  Maintenance mode. Thanks for your patience. Have a nice day')
                        logger_module.info('JiraAlerts program terminated')
                        exit(0)

                if value == '1':
                        logger_module.warning('System set to running on  test mode, this will runs as same as production mode but it will '
                                                   'not create a jira ticket nor delete the alert file')

                if value == '2':
                        logger_module.warning('System set to running on production mode, all features are up and running')

        logger_module.info('*******Start Running******')
        logger_module.info('Process number: ' + str(os.getpid()))
        initializer.main(value)
        logger_module.info('*******End Running*******')
