from flask import Flask, request
from app import app
from user.models import User
import os
from x import ocr

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()

@app.route('/imageUpload', methods=['POST'])
def imageUpload():
  f = request.files['file']  
  f.save((os.path.join(app.config['UPLOAD_FOLDER'], f.filename)))
  data = ocr(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))  
  return User().addData(data)
