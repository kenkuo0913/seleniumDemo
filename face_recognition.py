#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 22:12:16 2020

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

import dlib
import numpy as np
import cv2
import pandas as pd
import os

# face recognition model, the object maps human faces into 128D vectors
# Refer this tutorial: http://dlib.net/python/index.html#dlib.face_recognition_model_v1
facerec = dlib.face_recognition_model_v1("/Users/kenkuo/KNN_facial_recognition/dlib_face_recognition_resnet_model_v1.dat")


# Compute the e-distance between two 128D features
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


if os.path.exists("data/features_all.csv"):
    path_features_known_csv = "data/features_all.csv"
    csv_rd = pd.read_csv(path_features_known_csv, header=None)

    # The array to save the features of faces in the database
    features_known_arr = []

    # Print known faces
    for i in range(csv_rd.shape[0]):
        features_someone_arr = []
        for j in range(0, len(csv_rd.iloc[i])):
            features_someone_arr.append(csv_rd.iloc[i][j])
        features_known_arr.append(features_someone_arr)
    print("Faces in Database：", len(features_known_arr))

    # The detector and predictor will be used
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('/Users/kenkuo/KNN_facial_recognition/shape_predictor_68_face_landmarks.dat')

    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        flag, img_rd = cap.read()
        faces = detector(img_rd, 0)

        # font to write later
        font = cv2.FONT_ITALIC

        # The list to save the positions and names of current faces captured
        pos_namelist = []
        name_namelist = []
        person_list = os.listdir("data/data_faces_from_camera/")
        # remove .DS_Store if OS is MAC
        person_list.remove('.DS_Store')
        kk = cv2.waitKey(1)

        # press 'q' to exit
        if kk == ord('q'):
            break
        else:
            # face detected
            if len(faces) != 0:
                # Get the features captured and save into features_cap_arr
                features_cap_arr = []
                for i in range(len(faces)):
                    shape = predictor(img_rd, faces[i])
                    features_cap_arr.append(facerec.compute_face_descriptor(img_rd, shape))

                # 5. Traversal all the faces in the database
                for k in range(len(faces)):
                    print("##### camera person", k+1, "#####")
                
                    # Set the default names of faces with "unknown"
                    name_namelist.append("unknown")

                    # the positions of faces captured
                    pos_namelist.append(tuple([faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top())/4)]))

                    # For every faces detected, compare the faces in the database
                    e_distance_list = []
                    for i in range(len(features_known_arr)):
                        if str(features_known_arr[i][0]) != '0.0':
                            print("with ",person_list[i], "the e distance: ", end='')
                            e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                            print(e_distance_tmp)
                            e_distance_list.append(e_distance_tmp)
                        else:
                            e_distance_list.append(999999999)
                    # Find the one with minimum e distance
                    similar_person_num = e_distance_list.index(min(e_distance_list))
                    print("Minimum e distance with person", person_list[similar_person_num])
                    
                    if min(e_distance_list) < 0.4:
                        name_namelist[k] = person_list[similar_person_num]
                        print("May be person "+person_list[similar_person_num])
                    else:
                        print("Unknown person")

                    # draw rectangle
                    for kk, d in enumerate(faces):
                        cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
                    print('\n')

                # 6. write names under rectangle
                for i in range(len(faces)):
                    cv2.putText(img_rd, name_namelist[i], pos_namelist[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)

        print("Faces in camera now:", name_namelist, "\n")

        cv2.putText(img_rd, "Press 'q': Quit", (20, 450), font, 0.8, (84, 255, 159), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Face Recognition", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow("camera", img_rd)

    cap.release()
    cv2.destroyAllWindows()

else:
    print('##### Warning #####', '\n')
    print("'features_all.py' not found!")
    print("Please run 'get_faces_from_camera.py' and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'", '\n')
    print('##### Warning #####')