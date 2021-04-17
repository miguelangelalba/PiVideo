#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
import paramiko
from datetime import datetime, time
import os 
import re
#from camera import timestamp
from loggerFormat import logsFormat

#Const
#I don't need password since i have the public key on the server.
SERVER = '192.168.1.80'
USER = 'root'
PI_PATH = '/media/pi/00A3-22621/myVideos/'
SERVER_PATH = '/sharedfolders/PiCamera/'
REGISTER_NAME = "register.txt"
REGISTER_NAME_TO_DELATE = "registerToDelete.txt"
LOG_FILE_NAME = 'camera.log'

#Log 
logger = logsFormat(__name__,PI_PATH,LOG_FILE_NAME)

def sshLogin(server,user):
    try:
        sshClientLogin = paramiko.SSHClient()
        sshClientLogin.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        sshClientLogin.connect(server, username = user)
        logger.info('Conexión con el ' + server + ' establecida')
        return sshClientLogin

    except paramiko.ssh_exception.AuthenticationException as e:
        logger.error('Contraseña incorrecta' + str(e))

def sshLogout(sshClient):
    sshClient.close()
    logger.info('Cerrando conexión')

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
    logger.info('Archivos localizados en memoria: ' + str(contentsToSend))

    return contentsToSend

if __name__ == '__main__':
    try:
        logger.info(Files(PI_PATH))
        #sshClient = sshLogin(SERVER,USER)
        #scpClient = scptransfer(sshClient,FILE,DESTINATION_PATH)
        #Files(PI_PATH)
        #sshLogout(sshClient)

        #for i in range(10):

        #    recName = "Linea " + str(i)
        #    recRegister(PI_PATH,REGISTER_NAME,'recName')
        #fileReader(REGISTER_NAME,SERVER_PATH)
        #delLineStrings("Linea 4",REGISTER_NAME,SERVER_PATH)

    except paramiko.ssh_exception.AuthenticationException as e:
        logger.warning('Contraseña incorrecta' + str(e))