import re
from functions.config import storage
import requests


def detect_number(next_img,m):
    storage.child("defaulter_images_without_number/"+str(next_img)+str(m)+".jpg").put('defaulter'+str(next_img)+'.jpg')
    regions = ['mx', 'in'] 
    storage.child("defaulter_images_without_number/"+str(next_img)+str(m)+".jpg").download('defaulter'+str(next_img)+'.jpg')
    with open('defaulter'+str(next_img)+'.jpg', 'rb') as fp:
        response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                headers={'Authorization': 'Token 55a45b05aeb49ddd39178e7acd7261909181ecbc'})
        pairs=response.json().items()
        for key,value in pairs:
            if key=='results':
                if(len(value)>0):
                    for val in value:
                        v=val.items()
                        for plate,number in v:
                            if(plate=='plate' and len(number)==10):
                                print(number)
                                storage.child("defaulter_images/"+number+".jpg").put('defaulter'+str(next_img)+'.jpg')
                                return number

    return None                           
