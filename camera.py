#!/usr/bin/python3
# -*- coding: utf-8 -*-

from picamera import PiCamera
from datetime import datetime, time
import os
from fileHandler import *
import threading

#Const
SERVER = '192.168.1.80'
USER = 'pi'
SERVER_PATH = '/media/pi/Seagate Expansion Drive/PiCamera'
PI_PATH = '/media/pi/276E-0D81/'
REGISTER_NAME = 'register.txt'
REGISTER_NAME_TO_DELATE = 'registerToDelete.txt'


def timestamp():
    return datetime.now().isoformat(timespec= 'seconds')
    #Returns a timsStam at the instant it runs in the function in ISO format.

def createDirRec(folderName):
    try:
        os.mkdir(PI_PATH + folderName)
        print ('Creando folder ' + folderName)
    except OSError as e:
        print(e)
def rec (camera,folderName,path,ts,regName,regDelName):
    #I hace to format the timestamp becouse Raspivid doesn't accept the ":" in a file name.
    
    ts = ts.replace(':','')
    recName = ts + '.h264'
    pathRecName = path + folderName + '/' + recName
    camera.resolution = (1920, 1080)
    camera.exposure_mode = ('night')
    camera.clock_mode = ('raw')
    camera.framerate = (5)
    camera.start_preview()
    camera.annotate_text = timestamp()
    print(timestamp() + " Grabando archivo: " + recName)
    camera.start_recording(pathRecName,sps_timing=True,bitrate=10000000)
    camera.wait_recording(3600)
    camera.stop_recording()
    print(timestamp() + " Grabación finalizada archivo: " + recName)
    recRegister(path,regName,recName)
    recRegisterToDelete(path,regDelName,recName)
    return recName

if __name__ == "__main__":

    folder = 'myVideos'
    #path = '/media/pi/0113-44041/'
    camera = PiCamera()
    try:
        createDirRec(folder)
        ts = timestamp()
        recName = rec(camera,folder,PI_PATH,ts,REGISTER_NAME,REGISTER_NAME_TO_DELATE)
        sshClient = sshLogin(SERVER,USER)
        t1 = threading.Thread(name = "thread1",target=scptransfer,args=(sshClient,PI_PATH,SERVER_PATH,REGISTER_NAME_TO_DELATE,recName))
        t1.start()
        ts = timestamp()
        recName = rec(camera,folder,PI_PATH,ts,REGISTER_NAME,REGISTER_NAME_TO_DELATE)
    finally:

        print(timestamp() + "Cerrando cámara")
        camera.close()
        sshLogout(sshClient)
        t1.join()
