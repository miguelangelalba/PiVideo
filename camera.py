#!/usr/bin/python3
# -*- coding: utf-8 -*-

from picamera import PiCamera
from time import sleep

#Const

def rec (camera):
    camera.resolution = (1920, 1080)
    camera.start_preview()
    camera.start_recording('/media/pi/0113-44041/my_video.h264')
    camera.wait_recording(60)
    camera.stop_recording()


if __name__ == "__main__":

    camera = PiCamera()
    try:
        
        rec(camera)

    finally:

        print("Grabación finalizada")
        camera.close()