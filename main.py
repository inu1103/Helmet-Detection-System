import os
import uuid
import flask
import urllib
from flask import Flask , render_template  , request , send_file
import functions.detect as detect
import functions.extract_frames as extract_frames
import functions.config as config
import functions.fetch_images as images
from flask_paginate import Pagination, get_page_parameter


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

ALLOWED_VIDEXT = set(['mp4'])
def allowed_vidfile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_VIDEXT

token="&token=3b377f6a-2dba-4ddb-9079-791da2cbd662"

app = Flask(__name__)


@app.route('/')
def home():
        return render_template("index.html")

@app.route('/detect_img',methods = ['GET' , 'POST'])
def detect_helmet():
        next_img_=int(config.database.child('counter').get().val().get('value'))+1
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            target_path=os.path.join(os.getcwd() , 'static/images')
            file.save(os.path.join( target_path, file.filename))
            img_path = os.path.join(target_path, file.filename)
            img = file.filename
        number=detect.detect(img_path)
        os.remove(img_path)
        size=len(number)
        img_path_next=config.storage.child("images/" + str(next_img_)+".jpg").get_url(None)
        return render_template('detected.html',number=number,img=img,size=size,path=str(img_path_next),img_number=str(next_img_))

@app.route('/detect_video',methods = ['GET' , 'POST'])
def detect_helmet_video():
        next_img_before=int(config.database.child('counter').get().val().get('value'))+1
        file = request.files['file']
        if file and allowed_vidfile(file.filename):
            target_path=os.path.join(os.getcwd() , 'static/images')
            file.save(os.path.join( target_path, file.filename))
            vid_path = os.path.join(target_path, file.filename)
            vid = file.filename
        extract_frames.extract(vid_path)
        next_img_after=int(config.database.child('counter').get().val().get('value'))+1          
        return render_template('videoFrames.html',start=range(next_img_before,next_img_after),frame_number=next_img_before)

@app.route('/fetch_number',methods = ['GET' , 'POST'])
def fetch_image():
        number=request.form.get("number")
        print(number)
        url_img=images.getnumber(number)
        print(url_img)
        return render_template("show.html",number="yes",url_img=url_img+token)

@app.route('/fetch_detected/<img_number>',methods = ['GET'])
def fetch_detcted_image(img_number):
        url_img=images.getImage(img_number)
        return render_template("show.html",number="no",url_img=url_img+token)


@app.route('/fetch_number_plates/<img_number>',methods = ['GET'])
def fetch_number_image(img_number):
        urls_img=images.getNumberPlateImage(img_number)
        return render_template("numberPlates.html",urls_img=urls_img)

@app.route('/fetch_defaulted/<img_number>',methods = ['GET'])
def fetch_defaulter_images(img_number):
        urls_img=images.getDefaulterImage(img_number)
        return render_template("listDefaulters.html",urls_img=urls_img)

@app.route('/fetch_frames/<img_number>',methods = ['GET'])
def fetch_frames(img_number):
        img_path_next=config.storage.child("images/"+str(img_number)+".jpg").get_url(None)
        return render_template('detected.html',size=0,path=str(img_path_next),img_number=str(img_number))

