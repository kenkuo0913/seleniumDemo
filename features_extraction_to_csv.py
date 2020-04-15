#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:50:54 2020

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

import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np

# 要讀取人臉圖像文件的路徑
path_images_from_camera = "data/data_faces_from_camera/"

# Dlib 正向人臉檢測器
detector = dlib.get_frontal_face_detector()

# Dlib 人臉預測器
predictor = dlib.shape_predictor("/Users/kenkuo/KNN_facial_recognition/shape_predictor_68_face_landmarks.dat")

# Dlib 人脸識別模型
# Face recognition model, the object maps human faces into 128D vectors
face_rec = dlib.face_recognition_model_v1("/Users/kenkuo/KNN_facial_recognition/dlib_face_recognition_resnet_model_v1.dat")


# 返回單張圖像的128D特徵
def return_128d_features(path_img):
    img_rd = io.imread(path_img)
    faces = detector(img_rd, 1)

    print("%-40s %-20s" % ("image with faces detected:", path_img), '\n')

    # faces detected
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_rec.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
        print("no face")

    return face_descriptor


# 将文件夾中照片特徵提取出来,寫入CSV
def return_features_mean_personX(path_faces_personX):
    features_list_personX = []
    photos_list = os.listdir(path_faces_personX)
    if photos_list:
        for i in range(1,len(photos_list)):
            # run func return_128d_features()
            print("%-40s %-20s" % ("image to read:", path_faces_personX + "/" + photos_list[i]))
            features_128d = return_128d_features(path_faces_personX + "/" + photos_list[i])
            #  print(features_128d)
            # no face
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
    else:
        print("Warning: No images in " + path_faces_personX + '/', '\n')

    # calculate mean of 128D features
    # personX 的 N 張圖像 x 128D -> 1 x 128D
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX).mean(axis=0)
    else:
        features_mean_personX = '0'

    return features_mean_personX


# get the num of latest person
person_list = os.listdir("data/data_faces_from_camera/")
# remove .DS_Store if OS is MAC
person_list.remove('.DS_Store')
# person_num_list = []
# for person in person_list[1:]:
    # person_num_list.append(int(person.split('_')[-1]))
# person_cnt = max(person_num_list)

with open("data/features_all.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for person in person_list:
        # Get the mean/average features of face/personX, it will be a list with a length of 128D
        print(path_images_from_camera + person)
        features_mean_personX = return_features_mean_personX(path_images_from_camera + person)
        writer.writerow(features_mean_personX)
        print("The mean of features:", list(features_mean_personX))
        print('\n')
    print("Save all the features of faces registered into: data/features_all.csv")