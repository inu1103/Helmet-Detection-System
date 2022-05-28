from re import S
from functions.config import storage
from urllib.request import urlopen
from urllib.error import *

def getnumber(input):
    print(storage)
    return storage.child("defaulter_images/" + input+".jpg").get_url(None)

def getImage(input):
    return storage.child("detected_images/"+input+".jpg").get_url(None)

def getNumberPlateImage(input):
    imageIsThere=True
    m=1
    image_paths=[]
    while(imageIsThere):
        urltemp=storage.child("number_plates/"+input+str(m)+".jpg").get_url(None)
        try:
            urlopen(urltemp)
        except HTTPError as e:
            print("HTTP error", e)
            break
     
        except URLError as e:
            break
 
        else:
            image_paths.append(storage.child("number_plates/"+input+str(m)+".jpg").get_url(None))
            m=m+1
    return image_paths

def getDefaulterImage(input):
    imageIsThere=True
    m=1
    image_paths=[]
    while(imageIsThere):
        urltemp=storage.child("defaulter_images_without_number/"+input+str(m)+".jpg").get_url(None)
        try:
            urlopen(urltemp)
        except HTTPError as e:
            print("HTTP error", e)
            break
     
        except URLError as e:
            break
 
        else:
            image_paths.append(storage.child("defaulter_images_without_number/"+input+str(m)+".jpg").get_url(None))
            m=m+1
    return image_paths