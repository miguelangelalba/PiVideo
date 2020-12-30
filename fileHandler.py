#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scp
import paramiko
import time
from getpass import getpass

#Const
Server = '192.168.1.80'
User = 'pi'

if __name__ == '__main__':
    try:

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

        password = getpass('Ingrese su contraseña: ')
        client.connect(Server, username=User, password=password)

        stdin, stdout, stderr = client.exec_command('ls')

        time.sleep(1)
        result = stdout.read().decode()

        print (result)
        client.close()
    except paramiko.ssh_exception.AuthenticationException as e:
        print('Contraseña incorrecta')