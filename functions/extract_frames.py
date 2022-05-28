import cv2
import functions.detect as detect
import os

def extract(vid_path):
    video = cv2.VideoCapture(vid_path)
    i=0
    currentframe = 0
    frame_skip=30
    while(True):
        ret,frame = video.read()
        if not ret:
            break
        if i > frame_skip-1:
            cv2.imwrite( "tempVideoFrame.jpg",frame)
            detect.detect("tempVideoFrame.jpg")
            os.remove("tempVideoFrame.jpg")
            currentframe += 1
            i=0
            continue
        i+=1