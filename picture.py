#! /usr/bin/env python3
import picamera as _picamera
import datetime as _dt

PICTURE_FOLDER = "/home/pi/pictures/"
camera = _picamera.PiCamera()
# camera.rotation = 180

def take_picture() -> str:
    """ takes a picture, stores it locally and returns the filepath """
    filename = PICTURE_FOLDER + str(_dt.datetime.now()) + ".jpg"
    camera.capture(filename)
    return filename


if __name__ == "__main__":
    take_picture()