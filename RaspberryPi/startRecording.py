from picamera import PiCamera
from time import sleep
import sys
import datetime

duration = sys.argv[1]
numberOfVideos = sys.argv[2]

f=open("videoMetaData.txt", "a+")
f.truncate(0)
counter = 0
camera = PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 30
camera.start_preview()
while counter < int(numberOfVideos):
        camera.start_recording('./videoBuffer/video' + str(counter) + '.h264')
        f.write("%d started %s %s\n" %(counter, "location",datetime.datetime.now())) #video number, status, location, datetime
        sleep(int(duration))
        camera.stop_recording()
        f.write("%d ended %s %s\n" %(counter, "location", datetime.datetime.now()))
        counter += 1
camera.stop_preview()
