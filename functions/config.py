import cv2
import numpy as np
import requests
import firebase_admin 
import os
import functions.detect_number_plate as detect_number_plate
import pyrebase
import sys

config = {
        "apiKey": "AIzaSyCFdA7Nv3IAL8m9wQHYRdfdp9pJaGaOCV0",
    "authDomain": "hdst-7ef0f.firebaseapp.com",
    "databaseURL": "https://hdst-7ef0f-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "hdst-7ef0f",
    "storageBucket": "hdst-7ef0f.appspot.com",
    "messagingSenderId": "121051057217",
    "appId": "1:121051057217:web:e0c255ef641e2575088ac0",
    "measurementId": "G-91LEBWJJLP",
    "serviceAccount": "./keys/hdst-7ef0f-firebase-adminsdk-rwskm-5cf7de6e68.json"
    }
firebase = pyrebase.initialize_app(config)
storage=firebase.storage()
database= firebase.database()       
net = cv2.dnn.readNet('./weights/yolov3_training_final.weights', './cfg/yolov3_testing.cfg')
with open("./classes/classes.txt", "r") as f:
    classes = f.read().splitlines()
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))
net_number = cv2.dnn.readNet('./weights/yolov3_training_final_number_plate.weights', './cfg/yolov3_testing_number_plate.cfg')
classes_number = []
with open("./classes/classes_number_plate.txt", "r") as f:
    classes_number = f.read().splitlines()
font_number = cv2.FONT_HERSHEY_PLAIN
colors_number = np.random.uniform(0, 255, size=(100, 3))