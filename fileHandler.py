#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
import paramiko
from datetime import datetime, time

#Const
#I don't need password since i have the public key on the server.
SERVER = '192.168.1.80'
USER = 'pi'
FILE = '/media/pi/0113-44041/myVideos/2020-12-30T204223.h264'
DESTINATION_PATH = '/media/pi/Seagate Expansion Drive/PiCamera'
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

def closeClients(sshClientLogout,scpClient):
    sshClientLogout.close()
    scpClient.close()

def scptransfer(sshClient,origin,destination):
    
    scpClient = scp.SCPClient(sshClient.get_transport())
    print ('Trasnfiriendo archivo:' + origin + datetime.now().isoformat(timespec= 'seconds'))
    scpClient.put(origin,destination)
    print ('Archivo trasnferido: ' + datetime.now().isoformat(timespec= 'seconds'))

    return scpClient

def recRegister (recName,pathRegister):

    #register = open(pathRegister + REGISTER_NAME,"a")
    register = open(recName,"a")
    register.write(recName + "\n")
    register.close()

def recRegisterToDelete (recName,pathRegister):
    
    register = open(pathRegister + recName,"a")
    register.write(recName + ".\n")
    register.close()

def fileReader (fileName,path):
    #This function in the future can will delete. It's just to make some proves.
    f = open(fileName,"r")
    print(f.read())
    f.close()
    return f

def delLineStrings(recName,fileName,path):

    f = open(fileName,"r")
    lines = f.readlines()
    f.close
    f = open(fileName,"w")

    for line in lines:
        if line!=recName +"\n":
            f.write(line)



if __name__ == '__main__':
    try:
        #sshClient = sshLogin()
        #scpClient = scptransfer(sshClient,FILE,DESTINATION_PATH)
        #closeClients(sshClient,scpClient)

        for i in range(10):

            recName = "Linea " + str(i)
            recRegister(recName,"/")
        fileReader(REGISTER_NAME,DESTINATION_PATH)
        delLineStrings("Linea 4",REGISTER_NAME,DESTINATION_PATH)

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Contraseña incorrecta')