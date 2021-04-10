#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
#import paramiko
from datetime import datetime, time
import os 
import re
from pathlib import Path
#from camera import timestamp

#Const
#I don't need password since i have the public key on the server.
SERVER = '192.168.1.80'
USER = 'root'
PI_PATH = '/media/pi/276E-0D81/myVideos/'
SERVER_PATH = '/sharedfolders/PiCamera/'
REGISTER_NAME = "register.txt"
REGISTER_NAME_TO_DELATE = "registerToDelete.txt"

def timestamp():
    return datetime.now().isoformat()
    #Returns a timsStam at the instant it runs in the function in ISO format.

def scptransfer(sshClient,origin,destination,regDelName,recName):
    
    pathOriginName = origin + recName 
    scpClient = scp.SCPClient(sshClient.get_transport())
    print ( timestamp() + ' Trasnfiriendo archivo: ' + pathOriginName)
    scpClient.put(pathOriginName,destination)
    print (timestamp() + ' Archivo trasnferido a:' + destination)
    recRegisterToDelete(origin,regDelName,recName)
    scpClient.close()

def recRegister (pathRegister,registerName,recName):

    register = open(pathRegister + registerName,"a")
    print (timestamp() + ' Se ha añadido la grabación a ' + registerName)
    #register = open(recName,"a")
    register.write(recName + "\n")
    register.close()

def recRegisterToDelete (pathRegister,regDelName,recName):
    # I have to create a function to check if the file existis or not
    print("Añadiendo: " + recName )
    register = open(pathRegister + regDelName,"a")
    register.write(recName + "\n")
    register.close()

def fileReader (path,fileName):
    #This function in the future can will delete. It's just to make some proves.
    f = open(fileName,"r")
    print(f.read())
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
            print (timestamp() + ' Archivo: ' + recName + ' borrado')

def readLines(path,fileName):
    pathFileName = path + fileName
    f = open(pathFileName,"r")
    lines = f.readlines()
    f.close
    return lines

def removeFile(path,regToDelete):

    lines = readLines(path,regToDelete)

    for line in lines:
        pathRecName = path + line
        os.remove(pathRecName.replace('\n',""))
        print (timestamp() + ' Archivo: ' + line + ' borrado')
        delLineStrings(path,line,regToDelete)    

def Files(path):
    contents = os.listdir(path)
    contentsToSend = []
    for content in contents:
        if re.search('(?<=).h264',content):
            contentsToSend.append(content)
    #print (timestamp() + ' Archivos no enviados: ' + str(contentsToSend))
    return contentsToSend

if __name__ == '__main__':
    print (Files(PI_PATH))
    #sshClient = sshLogin(SERVER,USER)
        #scpClient = scptransfer(sshClient,FILE,DESTINATION_PATH)
        #Files(PI_PATH)
        #sshLogout(sshClient)

        #for i in range(10):

        #    recName = "Linea " + str(i)
        #    recRegister(PI_PATH,REGISTER_NAME,'recName')
        #fileReader(REGISTER_NAME,SERVER_PATH)
        #delLineStrings("Linea 4",REGISTER_NAME,SERVER_PATH)