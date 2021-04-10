#!/usr/bin/python3
# -*- coding: utf-8 -*-

from fileHandlerServer import Files, recRegisterToDelete
from datetime import datetime, time
import os
#import numpy as np
import shutil

SERVER_PATH = '/sharedfolders/PiCamera/'
REGISTER_NAME_TO_DELATE = 'registerToDelete.txt'


def timestamp():
    return datetime.now().isoformat()

def filesCopy(dic):

    for key,value in dic.items():
        
        for nameFile in value:
            
            #shutil.copy(dic[nameFodelr[]])
            recRegisterToDelete(SERVER_PATH,REGISTER_NAME_TO_DELATE,nameFile)
            print (timestamp() + " Archivo copiado: " + key + ":" + nameFile)


def createDir(dirName):
    #This funciton creates Directories
    try:
        #os.mkdir(SERVER_PATH + dirName)
        print (timestamp() + 'Creando Directorio:  ' + dirName)
    except OSError as e:
        print(timestamp() + e)


def checkFilesTime(list):
    # Dictionary file organization
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
        print ("Imprimiendo 2: " + str(dic))
        filesCopy(dic)

    finally:
        print ("Terminando script")