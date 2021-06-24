# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 21:27:34 2021

@author: Harsh Chaudhary
"""
import cv2
import mediapipe as mp
import time
import math
import screen_brightness_control as sbc
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import autopy

wScr, hScr = autopy.screen.size()

px, py = 0, 0
cx, cy = 0, 0

prevTime = 0
currTime = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 420)

while True:
    _, image = video.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    cv2.rectangle(image, (100, 100), (640-100, 420-100), (255, 0, 255), 3)
    
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            h, w, c = image.shape
            x1, x2, y1, y2 = 0, 0, 0, 0
            
            lm = handlms.landmark[8]
            x1, y1 = int(lm.x * w), int(lm.y * h)
            
            X = np.interp(x1, (100, 640-100), (0, wScr))
            Y = np.interp(y1, (100, 420-100), (0, hScr))
            
            cx = px + (X-px)/5
            cy = py + (Y-py)/5
            
            autopy.mouse.move(wScr-cx, cy)
            px, py = cx, cy  
            
            lm = handlms.landmark[12]
            x2, y2 = int(lm.x * w), int(lm.y * h)
            
            cv2.circle(image, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
            # cv2.circle(image, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
            # cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            
            D = math.hypot(x2-x1, y2-y1)
            D = int(np.interp(D, [25, 250], [0, 100]))
            D = 6 * round(D/6)
            if D == 0:
                cv2.circle(image, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
            # sbc.set_brightness(D)

    
    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime
    
    cv2.putText(image, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 255, 2)
    cv2.imshow('Stream', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
video.release()
# Destroy all the windows
cv2.destroyAllWindows()

