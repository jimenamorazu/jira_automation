#!/usr/bin/python
from ParsingServiceOutPut import ParsingServiceOutPut


class MultipleJiraTicket:
	def __init__(self):
		pass

	def multipleprocesscreation(self, myparsingdata):
		details = []
		mycol = []
		totaljira = 0

		if myparsingdata[5].find("<br>") > -1:
			pservice = ParsingServiceOutPut()
			mycol, details, total_jira = pservice.serviceoutputparsing(myparsingdata[5])

		else:
			if myparsingdata[5]:
				total_jira = 1
				details.append(myparsingdata[5])

		return mycol, details, total_jira
