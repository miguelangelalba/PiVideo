#!/usr/bin/python3
# -*- coding: utf-8 -*-

from fileHandlerServer import Files
from datetime import datetime, time
import os
import numpy as np

SERVER_PATH = '/sharedfolders/PiCamera/'


def timestamp():
    return datetime.now().isoformat(timespec= 'seconds')

def createDirRec(dirName):
    try:
        os.mkdir(SERVER_PATH + dirName)
        print ('Creando folder ' + dirName)
    except OSError as e:
        print(timestamp() + e)


def checkFilesTime(list):
    oldName = ""
    dic = {}

    for file in list:
        nameFile = file.split ("T")
        if nameFile != oldName[0]:
            dic = dic.setdefault(nameFile,np.array([file]))
        oldName = nameFile[0]
        print (nameFile)



if __name__ == '__main__':

    try:
        files = Files(SERVER_PATH)
        print (files)
        checkFilesTime(files)

    finally:
        print ("Terminando script")