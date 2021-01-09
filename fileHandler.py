#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
import paramiko
from datetime import datetime, time
import os 
import re
from camera import timestamp

#Const
#I don't need password since i have the public key on the server.
SERVER = '192.168.1.80'
USER = 'pi'
PI_PATH = '/media/pi/276E-0D81/myVideos/'
SERVER_PATH = '/media/pi/Seagate Expansion Drive/PiCamera'
REGISTER_NAME = "register.txt"
REGISTER_NAME_TO_DELATE = "registerToDelete.txt"

def sshLogin(server,user):
    try:
        sshClientLogin = paramiko.SSHClient()
        sshClientLogin.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        sshClientLogin.connect(server, username=user)
        print('Conexión con el ' + server + ' establecida')
        return sshClientLogin
    except paramiko.ssh_exception.AuthenticationException as e:
        print('Contraseña incorrecta')

def sshLogout(sshClient):
    sshClient.close()

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
    print (timestamp() + ' Archivos no enviados: ' + str(contentsToSend))
    return contentsToSend

if __name__ == '__main__':
    try:
        print (Files(PI_PATH))
        #sshClient = sshLogin()
        #scpClient = scptransfer(sshClient,FILE,DESTINATION_PATH)
        #closeClients(sshClient)

        #for i in range(10):

        #    recName = "Linea " + str(i)
        #    recRegister(PI_PATH,REGISTER_NAME,'recName')
        #fileReader(REGISTER_NAME,SERVER_PATH)
        #delLineStrings("Linea 4",REGISTER_NAME,SERVER_PATH)

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Contraseña incorrecta')