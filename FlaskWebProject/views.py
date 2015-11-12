#!/usr/bin/python
# -*- coding: utf8 -*-

# Please install requests first if you don't have it: pip install requests
import requests
import hmac
import hashlib
import base64
import time
import re
import ntpath
import cv2
from flask import request
from flask import make_response
from flask import render_template
from FlaskWebProject import app
from flask import Flask, jsonify

# URL Endpoint to post the data
REQUEST_URL = "https://apisandbox.moxtra.com/oauth/token"

# URL Endpoint to post the data
UPLOAD_URL = "https://sandbox.moxtra.com/board/upload"

# Moxtra App Credentials from developer.moxtra.com
client_id = "oHeCjMRnDP4"
client_secret = "sxW5EyFjRyk"


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page'
    )
@app.route('/about')
def about():
    """Renders the home page."""
    return render_template(
        'aboutus.html',
        title='Home Page'
    )
@app.route('/second')
def signin():
    """Renders the home page."""
    return render_template(
        'index2.html',
        title='Sign In - 2'
    )
@app.route('/third')
def signin2():
    """Renders the home page."""
    return render_template(
        'index3.html',
        title='Sign In - 2'
    )

# Sentiment analysis
@app.route('/sentiment')
def sentiment():
    words = request.args.get('text')
    params = {
        "text": words,
    }
    r = requests.post("http://text-processing.com/api/sentiment/", data= params)
    return make_response(r.text)

@app.route('/post/', methods=['POST'])
def hello():
    data = request.get_json()
    return jsonify({"text":data["text"]})

# Function to upload file
@app.route('/uploadFile')
def upload_page():
    # TODO: please change the sessionid, key, name...
    sessionid = request.args.get('session_id')
    sessionkey = request.args.get('session_key')
    filepath = request.args.get('file_path')

    
    head, tail = ntpath.split(filepath)

    params = {
            "type": "original",
            "sessionid": sessionid,
            "key": sessionkey,
            "name": tail,
            }

    with open(filepath, 'rb') as f:
        print filepath
        data = f.read()
        res = requests.post(UPLOAD_URL, params = params, data = data)
        print res.status_code
        print res.text
        response = make_response(res.text)
        

    return response


# Function to setup/initialize user and get access token
@app.route('/getAccessToken')
def get_access_token():

    
    
    # Unique ID of how user is identified in your system
    unique_id = request.args.get('uniqueid')
    
    
    
    # User Information
    firstname = "John"
    lastname = "Doe"
    
    # Create signature
    timestamp = str(int(time.time() * 1000))
    
    
    params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'http://www.moxtra.com/auth_uniqueid',
            'uniqueid': unique_id, 
            'timestamp': timestamp,
            'firstname': firstname,
            'lastname': lastname,
            }
    
    r = requests.post(REQUEST_URL, params = params)
    print r.status_code
    print r.text

    response = make_response(r.text)
    

    return response


if __name__ == '__main__':
    app.run()

