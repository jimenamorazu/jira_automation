#!/usr/bin/python

from os import listdir
from os.path import isfile, join


class ParsingShinken:
    __path = ''

    def __init__(self):
        pass

    @property
    def readfolder(self):
        error = ""
        onlyfiles = []

        try:
            onlyfiles = [f for f in listdir(self.get_path()) if isfile(join(self.get_path(), f))]
            return onlyfiles, error
        except OSError as e:
            error = e
            return onlyfiles, error

    def parsingfiles(self, path, files):
        # type: (object, object) -> object

        myParsingData = []
        error = ""

        try:

            infile = open(path + '/' + files[1], 'r')
        except OSError as e:
            error = e

        for line in enumerate(infile):
            myParsingData.append(line[1])
        infile.close()
	
	if len(myParsingData) == 0:
		error = 'Alert file empty'

        return myParsingData, error

    def get_path(self):
        return self.__path

    def set_path(self, newpath):
        self.__path = newpath
        return
