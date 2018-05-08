reload(sys)
sys.setdefaultencoding('utf8')


class JiraAlertsConfigFileReader:
        def __init__(self):

                try:
                        self.cfg = ConfigParser.ConfigParser()
                        self.cfg.read('/var/lib/shinken/production/jira_automation/JiraAutoConfig.cfg')
                except ConfigParser.ParsingError() as err:
                         "Could not parse:", err
                        exit()
                return

        def readconfiguration(self, section, option):
                value = ""
                error = ""
                try:
                        value = self.cfg.get(section, option)
                except ConfigParser.NoOptionError as err:
                        error = err
                except ConfigParser.NoSectionError as err:
                        error = err
                return value, error
