#!/usr/bin/python3
# -*- coding: utf-8 -*-

from picamera import PiCamera
from datetime import datetime, time
import os

#Const

def timestamp():
    dt = datetime.now()
    #Returns a timsStam at the instant it runs in the function.
    return dt.isoformat(timespec= 'seconds')

def createDirRec(folderName):
    try:
        os.mkdir('/media/pi/0113-44041/' + folderName)
        print ('Creando folder ' + folderName)
    except OSError as e:
        print(e)

def rec (camera,folderName,ts):
    #I hace to format the timestamp becouse Raspivid doesn't accept the ":" in a file name.
    ts = ts.replace(':','') 
    camera.resolution = (1920, 1080)
    camera.start_preview()
    camera.start_recording('/media/pi/0113-44041/' + folderName + '/' + ts + '.h264')
    camera.wait_recording(60)
    camera.stop_recording()


if __name__ == "__main__":

    folder = 'myVideos'
    camera = PiCamera()
    try:
        createDirRec(folder)
        ts = timestamp()
        rec(camera,folder,ts)

    finally:

        print("Grabación finalizada")
        camera.close()