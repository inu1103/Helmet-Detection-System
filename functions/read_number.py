import cv2
import pytesseract
import os
import numpy as np
import imutils
import easyocr


def read_number(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)
    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite("temp.jpg",img)
    os.remove("temp.jpg")
    return pytesseract.image_to_string(img)

def read_number1(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 30, 200) #Edge detection
        #plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        #plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        #plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        print(result)
        return result
    except:
        return "0"    