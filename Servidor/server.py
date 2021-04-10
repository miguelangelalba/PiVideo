#!/usr/bin/python3
# -*- coding: utf-8 -*-

from fileHandlerServer import Files
from datetime import datetime, time
import os
#import numpy as np
import shutil

SERVER_PATH = '/sharedfolders/PiCamera/'


def timestamp():
    return datetime.now().isoformat()

def filesCopy(dic):

    for nameFolder in dic:
        for nameFile in nameFolder:
            print (nameFile)
            #shutil.copy(dic[nameFodelr[]])


def createDir(dirName):
    try:
        os.mkdir(SERVER_PATH + dirName)
        print (timestamp() + 'Creando Directorio:  ' + dirName)
    except OSError as e:
        print(timestamp() + e)


def checkFilesTime(list):
    oldName = ""
    dic = {}
    auxList = [""]

    for file in list:
        nameDir = file.split ("T")
        #print ("Nombre de archivo: " + str(nameDir))
        if nameDir[0] != oldName:
            auxList = []
            dic[nameDir[0]] = [file]
            oldName = nameDir[0]
            #print(str(dic))
        else:
            dic[nameDir[0]].append(file)
    print ("Imprimiendo diccionario: " + str(dic))
    return dic

if __name__ == '__main__':

    try:
        files = Files(SERVER_PATH)
        print (timestamp() + str(files))
        dic = checkFilesTime(files)
        filesCopy(dic)

    finally:
        print ("Terminando script")