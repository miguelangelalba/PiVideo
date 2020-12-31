#!/usr/bin/python3
# -*- coding: utf-8 -*-

from picamera import PiCamera
from datetime import datetime, time
import os
from fileHandler import *

#Const
SERVER = '192.168.1.80'
USER = 'pi'
SERVER_PATH = '/media/pi/Seagate Expansion Drive/PiCamera'
PATH_REC_FOLDER = "/media/pi/276E-0D81/"

def timestamp():
    return datetime.now().isoformat(timespec= 'seconds')
    #Returns a timsStam at the instant it runs in the function in ISO format.

def createDirRec(folderName):
    try:
        os.mkdir(PATH_REC_FOLDER + folderName)
        print ('Creando folder ' + folderName)
    except OSError as e:
        print(e)

def rec (camera,folderName,path,ts):
    #I hace to format the timestamp becouse Raspivid doesn't accept the ":" in a file name.
    
    ts = ts.replace(':','')
    fileName = ts + '.h264'
    pathFileName = path + folderName + '/' + fileName
    camera.resolution = (1920, 1080)
    camera.exposure_mode = ('night')
    camera.clock_mode = ('raw')
    camera.framerate = (5)
    camera.start_preview()
    camera.annotate_text = timestamp()
    print("Grabando archivo: " + fileName + '' + ts)
    camera.start_recording(pathFileName,sps_timing=True,bitrate=10000000)
    camera.wait_recording(3600)
    camera.stop_recording()
    print("Grabación finalizada archivo: " + fileName + timestamp())
    return pathFileName

if __name__ == "__main__":

    folder = 'myVideos'
    #path = '/media/pi/0113-44041/'
    camera = PiCamera()
    try:
        createDirRec(folder)
        ts = timestamp()
        pathRec = rec(camera,folder,PATH_REC_FOLDER,ts)

        sshClient = sshLogin(SERVER,USER)
        scptransfer(sshClient,pathRec,SERVER_PATH)
        scpClient = scptransfer(sshClient,pathRec,SERVER_PATH)
        closeClients(sshClient,scpClient)

    finally:

        print("Cerramdo cámara")
        camera.close()
        closeClients(sshClient,scpClient)
