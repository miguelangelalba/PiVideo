#!/usr/bin/python3
# -*- coding: utf-8 -*-

from fileHandlerServer import Files, recRegisterToDelete, removeFile
import os
#import numpy as np
import shutil
from loggerFormat import logsFormat

#Const
SERVER_PATH = '/sharedfolders/PiCamera/'
REGISTER_NAME_TO_DELATE = 'registerToDelete.txt'
LOG_FILE_NAME = 'server.log'
#Logs

logger = logsFormat('server',SERVER_PATH,LOG_FILE_NAME)

def filesCopy(dic):

    for key,value in dic.items():
        
        for nameFile in value:
            folderPath = SERVER_PATH + "/" + key + "/"
            filePath = SERVER_PATH + "/" + nameFile
            shutil.copy(filePath,folderPath)
            recRegisterToDelete(SERVER_PATH,REGISTER_NAME_TO_DELATE,nameFile)
            logger.info('Archivo copiado: ' + key + '/cd ..' + nameFile)

def createDir(dirName):
    #This funciton creates Directories
    try:
        os.mkdir(SERVER_PATH + dirName)
        logger.info('Creando Directorio: ' + dirName)

    except OSError as e:
        logger.info(str(e))


def recHandler(list):
    # Dictionary file organization
    oldName = ""
    dic = {}

    for file in list:
        nameDir = file.split ("T")
        if nameDir[0] != oldName:
            dic[nameDir[0]] = [file]
            createDir(nameDir[0])
            oldName = nameDir[0]
        else:
            dic[nameDir[0]].append(file)
    logger.info('Imprimiendo diccionario: ' + str(dic))

    return dic

if __name__ == '__main__':

    try:
        files = Files(SERVER_PATH)
        dic = recHandler(files)
        filesCopy(dic)
        removeFile(SERVER_PATH,REGISTER_NAME_TO_DELATE)

    finally:
        logger.info('Terminando script')
