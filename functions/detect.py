import cv2
import numpy as np
import requests
import os
import functions.detect_number_plate as detect_number_plate
import functions.read_number_from_api as read_number_from_api
from functions.config import database,storage,net,colors,classes,font



def detect(img_path):
    
    next_img=int(database.child('counter').get().val().get('value'))+1

    database.child('counter').set({"value": str(next_img)})

    path_on_cloud = "images/"+str(next_img)+".jpg"

    storage.child(path_on_cloud).put(img_path)
    storage.child(path_on_cloud).download(str(next_img)+".jpg")

    img = cv2.imread(str(next_img)+".jpg")
    os.remove(str(next_img)+".jpg")

    answer=[]
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
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
            if confidence > 0.8:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)


    bike = []
    noHelmet = []
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
            if label=="Helmet":
                color=colors[0]
                print("helmet detected")
            if label=="No Helmet":
                color=colors[1]
                print("helmet not detected")
                noHelmet.append([x,y,w,h])
            if label=="Person with Bike":
                color=colors[2]
                bike.append([x,y,w,h])
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y+20), font, 1, (255,255,255), 2)


    cv2.imwrite(str(next_img)+'.jpg',img)
    storage.child("detected_images/"+str(next_img)+".jpg").put(str(next_img)+'.jpg')
    os.remove(str(next_img)+'.jpg')

#detect numbers for defaulters
    m=0
    for i in noHelmet:
        m=m+1
        hx,hy,hw,hh = i
        print(hx,hy,hw,hh)
        for j in range(0,len(bike)):
            number_plate=False
            bx,by,bw,bh = bike[j]
            if((hx<=bx+bw and hx>=bx)or (hx+hw<=bx+bw and hx+hw>=bx)) and ((hy<=by+bh and hy>=by)or (hy+hh<=by+bh and hh+hy>=by)):
                cv2.imwrite('defaulter'+str(next_img)+'.jpg',img[by:by+bh,bx:bx+bw])
                number=read_number_from_api.detect_number(next_img,m)
                if(number!=None):
                    answer.append(number)
                    number_plate=True
                    break
                if number_plate==False:
                    number=detect_number_plate.detect(next_img,m)
                    if(number!=None and len(number)==10):
                        storage.child("defaulter_images/"+number+".jpg").put('defaulter'+str(next_img)+'.jpg')
                        answer.append(number)
                        break
        try:
            os.remove('defaulter'+str(next_img)+'.jpg')   
        except:
            print("no frame found")             
    return answer


        