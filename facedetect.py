#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 07:22:56 2020

@author: kenkuo
"""


import cv2
import sys
from PIL import Image

def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)
    
    #視訊來源，可以來自一段已存好的視訊，也可以直接來自USB攝像頭
    cap = cv2.VideoCapture(camera_idx)                
    
    #告訴OpenCV使用人臉識別分類器
    classfier = cv2.CascadeClassifier(r"/Users/kenkuo/Downloads/opencv-4.1.0/data/haarcascades/haarcascade_frontalface_alt2.xml")
    
    #識別出人臉後要畫的邊框的顏色，RGB格式
    color = (0, 255, 0)
    
    while cap.isOpened():
        ok, frame = cap.read() #讀取一幀資料
        if not ok:            
            break  

        #將當前幀轉換成灰度影象
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
        
        #人臉檢測，1.2和2分別為圖片縮放比例和需要檢測的有效點數
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:            #大於0則檢測到人臉                                   
            for faceRect in faceRects:  #單獨框出每一張人臉
                x, y, w, h = faceRect        
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                        
        #顯示影象
        cv2.imshow(window_name, frame)        
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break        
    
    #釋放攝像頭並銷燬所有視窗
    cap.release()
    cv2.destroyAllWindows() 
    
if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        CatchUsbVideo("識別人臉區域", 0)