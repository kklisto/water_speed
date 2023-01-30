
#https://docs.opencv.org/3.4.1/d6/d00/tutorial_py_root.html

from __future__ import print_function

import argparse
from this import d
import numpy as np
import cv2
import math
import time

from numpy import linalg as LA
from PIL import Image

def computeOpticalFlow1(prev, curr):
    flow = cv2.calcOpticalFlowFarneback(curr, prev, flow=None, pyr_scale=0.5, levels=3, winsize=20, iterations=15, poly_n=5, poly_sigma=1.2, flags=cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
    return flow

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Read video file')
    parser.add_argument('video', help='input video filename')
    parser.add_argument('deltaT', help='input deltaT between frames', type=int)
    parser.add_argument(
        "--sec",
        default=0,
        help="input time of frame (>0 && <video length) in seconds",
        type=int,
    )
    parser.add_argument(
        "--out",
        default="out",
        help="Output name",
        type=str,
    )

    args = parser.parse_args()
    cap = cv2.VideoCapture(args.video)

    if (cap.isOpened() == False):
        print("ERROR: unable to open video: "+args.video)
        quit()

    deltaT=args.deltaT
    seconds=args.sec
    out=args.out

    print("Starting segmentation")

    previousFrames=[]
    previousFramesRGB=[]

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = seconds * fps
    print("FPS:", fps)
    #print("deltaT:", deltaT,"frame diff")
    #print("seconds:", seconds,"sec")

    while(cap.isOpened()):

        ret, frame = cap.read()

        if frames > 0:
            frames -= 1.0
            continue

        if (ret==False):
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height = gray.shape[0]
        width = gray.shape[1]

        if (len(previousFrames) >= deltaT):

            rgbPrev = previousFramesRGB.pop(0)
            prev = previousFrames.pop(0)

            im = Image.fromarray(rgbPrev)
            im.save(out+"_frame.png")
            # optic flow dense, for each pixel you get a vector from it's old positioning
            flow = computeOpticalFlow1(prev, gray)

            ## MORPHOMATH ##
            s = (height, width)
            test_flow = np.zeros(s)
            for y in range (height):
                for x in range (width):
                    test_flow[y, x] = LA.norm(flow[y, x])

            test = np.zeros(s)
            mean = np.mean(test_flow)
            std = np.std(test_flow)

            test [test_flow > mean] = 255
            kernel = np.ones((20,20),np.uint8)

            im = Image.fromarray(test)
            im = im.convert("RGB")
            #im.save(out+"_flow.png")

            test = cv2.morphologyEx(test, cv2.MORPH_CLOSE, kernel)
            

            im = Image.fromarray(test)
            
            # im = im.convert("RGB")
            # im.save(out+"_closing.png")

            test = cv2.morphologyEx(test, cv2.MORPH_OPEN, kernel)
            im = Image.fromarray(test)
            im = im.convert("RGB")
            #im.save(out+"_opening.png")
            break

            ## END MORPHOMATH ##
        previousFrames.append(gray.copy())
        previousFramesRGB.append(frame)


    cap.release()

    #print("result files "+out+"(_frame/_flow/opening).png")
    print("END")
    #print(gray.shape)

    #MatricePoints= np.array([])
    #MatricedePoints = np.argwhere(frame == 255)
    #np.save('ArrayBlanc', MatricedePoints)

