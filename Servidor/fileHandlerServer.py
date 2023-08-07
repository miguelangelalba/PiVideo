#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
#import paramiko
import os 
import re
from pathlib import Path
from loggerFormat import logsFormat
#from camera import timestamp

#Const
#I don't need password since i have the public key on the server.
SERVER = '192.168.1.80'
USER = 'root'
PI_PATH = '/media/pi/276E-0D81/myVideos/'
SERVER_PATH = '/sharedfolders/PiCamera/'
REGISTER_NAME = "register.txt"
REGISTER_NAME_TO_DELATE = "registerToDelete.txt"
LOG_FILE_NAME = 'server.log'


#Logs

logger = logsFormat(__name__,SERVER_PATH,LOG_FILE_NAME)

def scptransfer(sshClient,origin,destination,regDelName,recName):
    
    pathOriginName = origin + recName 
    scpClient = scp.SCPClient(sshClient.get_transport())
    logger.info('Trasnfiriendo archivo: ' + pathOriginName)
    scpClient.put(pathOriginName,destination)
    logger.info('Archivo ' + recName + ' trasnferido a:' + destination)
    recRegisterToDelete(origin,regDelName,recName)
    scpClient.close()

def recRegister (pathRegister,registerName,recName):

    register = open(pathRegister + registerName,"a")
    logger.info('Se ha añadido la grabación a ' + registerName)
    #register = open(recName,"a")
    register.write(recName + "\n")
    register.close()

def recRegisterToDelete (pathRegister,regDelName,recName):
    # I have to create a function to check if the file existis or not
    logger.info('Añadiendo: ' + recName)
    register = open(pathRegister + regDelName,"a")
    register.write(recName + "\n")
    register.close()

def fileReader (path,fileName):
    #This function in the future can will delete. It's just to make some proves.
    f = open(fileName,"r")
    logger.info(f.read())

    f.close()
    #for line  in f

    return f

def delLineStrings(path,recName,fileName):

    pathFileName = path + fileName
    lines = readLines(path,fileName)
    f = open(pathFileName,"w")

    for line in lines:
        if (line == recName):
            pass
        else:
            f.write(line)
            logger.info('Archivo: ' + recName + ' borrado')

def readLines(path,fileName):
    pathFileName = path + fileName
    f = open(pathFileName,"r")
    lines = f.readlines()
    f.close
    return lines

def removeFile(path,regToDelete):

    lines = readLines(path,regToDelete)
    i = 0
    for line in lines:
        i = i + 1
        pathRecName = path + line
        os.remove(pathRecName.replace('\n',""))
        logger.info('Archivo: ' + line + ' borrado' + str(i) + "/"+ str(len(lines)))

        delLineStrings(path,line,regToDelete)    

def Files(path):
    contents = os.listdir(path)
    contentsToSend = []
    for content in contents:
        if re.search('(?<=).h264',content):
            contentsToSend.append(content)
    return contentsToSend

if __name__ == '__main__':
    logger.info(Files(PI_PATH))
    #sshClient = sshLogin(SERVER,USER)
        #scpClient = scptransfer(sshClient,FILE,DESTINATION_PATH)
    f = Files(SERVER_PATH)
    print (f)
        #sshLogout(sshClient)

        #for i in range(10):

        #    recName = "Linea " + str(i)
        #    recRegister(PI_PATH,REGISTER_NAME,'recName')
        #fileReader(REGISTER_NAME,SERVER_PATH)
        #delLineStrings("Linea 4",REGISTER_NAME,SERVER_PATH)