#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
import paramiko
from datetime import datetime, time

#Const
#I don't need password since i have the public key on the server.
Server = '192.168.1.80'
User = 'pi'
File = '/media/pi/0113-44041/myVideos/2020-12-30T204223.h264'
DestinationPath = '/media/pi/Seagate Expansion Drive/PiCamera'

def sshLogin():
    try:
        sshClientLogin = paramiko.SSHClient()
        sshClientLogin.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        sshClientLogin.connect(Server, username=User)
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

if __name__ == '__main__':
    try:
        sshClient = sshLogin()
        scpClient = scptransfer(sshClient,File,DestinationPath)
        closeClients(sshClient,scpClient)
        
    except paramiko.ssh_exception.AuthenticationException as e:
        print('Contraseña incorrecta')