#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
import paramiko
from datetime import datetime, time
from os import remove
from camera import timestamp

#Const
#I don't need password since i have the public key on the server.
SERVER = '192.168.1.80'
USER = 'pi'
PI_PATH = '/media/pi/0113-44041/myVideos/'
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
    
    scpClient = scp.SCPClient(sshClient.get_transport())
    print ( timestamp() + ' Trasnfiriendo archivo: ' + origin)
    scpClient.put(origin,destination)
    print (timestamp + 'Archivo trasnferido a:' + destination)
    recRegisterToDelete(origin,regDelName,recName)
    scpClient.close()

def recRegister (pathRegister,registerName,recName):

    register = open(pathRegister + registerName,"a")
    #register = open(recName,"a")
    register.write(recName + "\n")
    register.close()

def recRegisterToDelete (pathRegister,regDelName,recName):
    
    register = open(pathRegister + recName,"a")
    register.write(recName + ".\n")
    register.close()

def fileReader (path,fileName):
    #This function in the future can will delete. It's just to make some proves.
    f = open(fileName,"r")
    print(f.read())
    f.close()
    return f

def delLineStrings(path,recName,fileName):

    f = open(fileName,"r")
    lines = f.readlines()
    f.close
    f = open(fileName,"w")

    for line in lines:
        if line!=recName +"\n":
            f.write(line)

def removeFile(path,recName):
    pathRecName = path + recName
    remove(pathRecName)



if __name__ == '__main__':
    try:
        #sshClient = sshLogin()
        #scpClient = scptransfer(sshClient,FILE,DESTINATION_PATH)
        #closeClients(sshClient)

        for i in range(10):

            recName = "Linea " + str(i)
            recRegister(PI_PATH,REGISTER_NAME,'recName')
        fileReader(REGISTER_NAME,SERVER_PATH)
        delLineStrings("Linea 4",REGISTER_NAME,SERVER_PATH)

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Contraseña incorrecta')