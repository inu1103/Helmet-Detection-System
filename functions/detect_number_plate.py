import cv2
import numpy as np 
import os
import functions.read_number as read_number
from functions.config import net_number as net ,classes_number as classes ,font_number as font ,colors_number as colors,storage

def detect(next_img,m):
    img=cv2.imread('defaulter'+str(next_img)+'.jpg')
    print(img)
    height, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0),swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3,0.8)

    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            if(x<0):
                x=0
            if(y<0):
                y=0
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            if label=="plate":
                print("plate detected")
                cv2.imwrite("temp_number.jpg",img[y:y+h,x:x+w])
                storage.child("number_plates/"+str(next_img)+str(m)+".jpg").put("temp_number.jpg")
                os.remove("temp_number.jpg")
                number=read_number.read_number1(img[y:y+h,x:x+w])
                if(len(number)==10):
                    return number  
                                 
    return "0"
