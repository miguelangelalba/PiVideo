#!/usr/bin/python3
# -*- coding: utf-8 -*-

from picamera import PiCamera
from datetime import datetime, time
import os
from fileHandler import *
from concurrent.futures import ThreadPoolExecutor

#Const
SERVER = '192.168.1.80'
USER = 'miguelangel'
SERVER_PATH = '/sharedfolders/PiCamera'
PI_PATH = '/media/pi/00A3-2262/'
FOLDER_NAME = 'myVideos'
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
def rec (camera,path,ts,regName,regDelName):
    #I hace to format the timestamp becouse Raspivid doesn't accept the ":" in a file name.
    
    ts = ts.replace(':','')
    recName = ts + '.h264'
    pathRecName = path + recName
    camera.resolution = (1920, 1080)
    camera.exposure_mode = ('night')
    camera.clock_mode = ('raw')
    camera.framerate = (5)
    camera.start_preview()
    camera.annotate_text = timestamp()
    print(timestamp() + " Grabando archivo: " + recName)
    camera.start_recording(pathRecName,sps_timing=True,bitrate=10000000)
    camera.wait_recording(60)
    camera.stop_recording()
    print(timestamp() + " Grabación finalizada archivo: " + recName)
    recRegister(path,regName,recName)
    return recName

def filesManagSend(files,server,user,origin,destination,regDelName):
    #This function it's exclisvie to send the file afeter record
    sshClient = sshLogin(server,user)
    i = 0
    for f in files:
        i = i + 1
        scptransfer(sshClient,origin,destination,regDelName,f)
        print(timestamp() + "Archivos transferidos: " + str(i) + "/" + str(len(files)))
    sshLogout(sshClient)

def fileManagSend(f,server,user,origin,destination,regDelName):
    #This function it's exclisvie to send the file afeter record
    sshClient = sshLogin(server,user)
    scptransfer(sshClient,origin,destination,regDelName,f)
    sshLogout(sshClient)

if __name__ == "__main__":

  
    #path = '/media/pi/0113-44041/'
    camera = PiCamera()
    files = []
    executor = ThreadPoolExecutor(max_workers=3)
    try:

        createDirRec(FOLDER_NAME)
        ts = timestamp()
        piPath = PI_PATH + FOLDER_NAME + '/'
        executor.submit(removeFile,piPath,REGISTER_NAME_TO_DELATE)
        files = Files(piPath)
        if len(files) > 0 :
            executor.submit(filesManagSend,files,SERVER,USER,piPath,SERVER_PATH,REGISTER_NAME_TO_DELATE)
            #removeFile(piPath,REGISTER_NAME_TO_DELATE)
        for i in range(3):
            print ("Pasada antes de grabar")
            recName = rec(camera,piPath,ts,REGISTER_NAME,REGISTER_NAME_TO_DELATE)
            #sshClient = sshLogin(SERVER,USER)
            executor.submit(fileManagSend,recName,SERVER,USER,piPath,SERVER_PATH,REGISTER_NAME_TO_DELATE)
            #executor.submit(scptransfer,sshClient,piPath,SERVER_PATH,REGISTER_NAME_TO_DELATE,recName)
            ts = timestamp()
            #recName = rec(camera,piPath,ts,REGISTER_NAME,REGISTER_NAME_TO_DELATE)
            print ("Después de grabar")
            print (str(i))

    finally:
        print(timestamp() + "Cerrando cámara")
        camera.close()
        #sshLogout(sshClient)
        removeFile(piPath,REGISTER_NAME_TO_DELATE)
        executor.shutdown(wait=True)