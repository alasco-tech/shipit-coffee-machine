#! /usr/bin/env python3
import datetime as _dt
import os as _os
import picamera as _picamera

PICTURE_FOLDER = "/home/pi/pictures/"

if not _os.path.exists(PICTURE_FOLDER):
    _os.makedirs(PICTURE_FOLDER)

camera = _picamera.PiCamera()
camera.rotation = 90

def take_picture() -> str:
    """ takes a picture, stores it locally and returns the filepath """
    filename = PICTURE_FOLDER + str(_dt.datetime.now()) + ".jpg"
    camera.capture(filename)
    return filename


if __name__ == "__main__":
    take_picture()