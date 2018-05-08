#!/usr/bin/python


#this class is to format the jira description in order to create a ticket with all the alerts contained on the alert file
#added the html tag to the alert description in order to create a table on jira ticket
#still missing refomat the html to create a prettier table, like table cell auto streching and different colors

#able to create the jira with the rigth information check https://jira.cheetahmail.com/browse/MON-26845 for further details

class JiraOneDescriptionProcess:
	def __init__(self):
		return

	def processoneticket(self, myparsingdata):

		description_detail = ""

		if (str(myparsingdata[6])[:-1]):
			SOP = str(myparsingdata[6])[:-1]
		else:
			SOP = 'SOP not found'

		host = str(myparsingdata[1])[:-1]
		alertname = str(myparsingdata[4])[:-1]
		alertime =  str(myparsingdata[10])[:-1]



		alert_detail = ''
		# if myparsingdata[5].find("<br>") > -1:
		alert_detail = myparsingdata[5]

		description_detail = 'This ticket has been triggered as a result of a CRITICAL event in the application.' \
							 + '\n\n' + 'Here are the alert details. Please take a look into this ' + '\n\n' \
							 + 'Host: ' + host + '\n' + 'Alert Name: ' + alertname + '\n' + 'Alert TimeStamp: ' \
							 + alertime + '\n\n' + 'This is the alert output' + '\n\n' + '{html}' + alert_detail + '{html}' \
							 + '\n\n' + 'Please follow the next SOP, in order to fix this alert ' + '\n\n' + '[SOP ' \
							 + SOP + ' |' + SOP + ']'

		return description_detail
