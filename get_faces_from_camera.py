#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 20:05:47 2020

@author: kenkuo
"""

'''
此程式碼參考下方ＧitHub進行修改
进行人脸录入 / face register
录入多张人脸 / support multi-faces

Author:   coneypo
Blog:     http://www.cnblogs.com/AdaminXie
GitHub:   https://github.com/coneypo/Dlib_face_recognition_from_camera
Mail:     coneypo@foxmail.com
'''


import numpy as np
import dlib
import cv2
import os
import shutil

# Dlib 正向人脸檢測器
detector = dlib.get_frontal_face_detector()

# 調用鏡頭
cap = cv2.VideoCapture(0)

# The counter for screen shoot
cnt_ss = 0

# The folder to save face images
current_face_dir = ""

# The directory to save images of faces
path_photos_from_camera = "data/data_faces_from_camera/"


# Mkdir for saving photos and csv
def pre_work_mkdir():

    #make folders to save faces images and csv
    if os.path.isdir(path_photos_from_camera):
        pass
    else:
        os.mkdir(path_photos_from_camera)


pre_work_mkdir()


# Delete the old data of faces
def pre_work_del_old_face_folders():

    folders_rd = os.listdir(path_photos_from_camera)
    for i in range(len(folders_rd)):
        shutil.rmtree(path_photos_from_camera+folders_rd[i])

    if os.path.isfile("data/features_all.csv"):
        os.remove("data/features_all.csv")

# pre_work_del_old_face_folders()

# Check people order: person_cnt
# If the old folders exists
# 在之前 person_x 的序号按照 person_x+1 开始录入 / Start from person_x+1
# if os.listdir("data/data_faces_from_camera/"):
#     # 获取已录入的最后一个人脸序号 / Get the num of latest person
#     person_list = os.listdir("data/data_faces_from_camera/")
#     person_num_list = []
#     for person in person_list:
#         person_num_list.append(int(person.split('_')[-1]))
#     person_cnt = max(person_num_list)


# Start from person_1
# else:
#     person_cnt = 0

person_cnt=0
# The flag to control if save
save_flag = 1

# The flag to check if press 'n' before 's'
press_n_flag = 0

while cap.isOpened():
    flag, img_rd = cap.read()
    # print(img_rd.shape)
    # It should be 480 height * 640 width in Windows and Ubuntu by default
    # Maybe 1280x720 in macOS

    kk = cv2.waitKey(1)

    # Faces
    faces = detector(img_rd, 0)

    # Font to write
    font = cv2.FONT_ITALIC

    # press 'n' to create the folders for saving faces
    if kk == ord('n'):
        person_cnt += 1
        person_name=input('Please enter your name.')
        # current_face_dir = path_photos_from_camera + "person_" + str(person_cnt)
        current_face_dir = path_photos_from_camera + person_name
        os.makedirs(current_face_dir)
        print('\n')
        print("Create folders: ", current_face_dir)

        cnt_ss = 0              # clear the cnt of faces
        press_n_flag = 1        # have pressed 'n'

    # Face detected
    if len(faces) != 0:
        # Show the rectangle box of face
        for k, d in enumerate(faces):
            # Compute the width and height of the box
            # (x,y), (寬度width, 高度height)
            pos_start = tuple([d.left(), d.top()])
            pos_end = tuple([d.right(), d.bottom()])

            # compute the size of rectangle box
            height = (d.bottom() - d.top())
            width = (d.right() - d.left())

            hh = int(height/2)
            ww = int(width/2)

            # the color of rectangle of faces detected
            color_rectangle = (255, 255, 255)

            # To judge over 480x640 or not(if os is Windows)
            if (d.right()+ww) > 1280 or (d.bottom()+hh > 720) or (d.left()-ww < 0) or (d.top()-hh < 0):
                cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                color_rectangle = (0, 0, 255)
                save_flag = 0
                if kk == ord('s'):
                    print("Please adjust your position")
            else:
                color_rectangle = (255, 255, 255)
                save_flag = 1

            cv2.rectangle(img_rd,
                          tuple([d.left() - ww, d.top() - hh]),
                          tuple([d.right() + ww, d.bottom() + hh]),
                          color_rectangle, 2)

            # Create blank image according to the shape of face detected
            img_blank = np.zeros((int(height*2), width*2, 3), np.uint8)

            if save_flag:
                # Press 's' to save faces into local images
                if kk == ord('s'):
                    # check if you have pressed 'n'
                    if press_n_flag:
                        cnt_ss += 1
                        for ii in range(height*2):
                            for jj in range(width*2):
                                img_blank[ii][jj] = img_rd[d.top()-hh + ii][d.left()-ww + jj]
                        cv2.imwrite(current_face_dir + "/img_face_" + str(cnt_ss) + ".jpg", img_blank)
                        print("Save into：", str(current_face_dir) + "/img_face_" + str(cnt_ss) + ".jpg")
                    else:
                        print("Please press 'N' before 'S'")

    # Show the numbers of faces detected
    cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    # Add some statements
    cv2.putText(img_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "N: Create face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

    # Press 'q' to exit
    if kk == ord('q'):
        break

    # Uncomment this line if you want the camera window is resizeable
    # cv2.namedWindow("camera", 0)

    cv2.imshow("camera", img_rd)

# Release camera and destroy all windows
cap.release()
cv2.destroyAllWindows()