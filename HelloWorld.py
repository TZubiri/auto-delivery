import os
from flask import Flask,redirect,request,flash
import sys
from lib.meli import Meli
import time

counter = 0
app = Flask(__name__)
app.secret_key = '***REMOVED***'

meli = Meli(client_id=3410176288430291, client_secret="***REMOVED***")

@app.route('/userstart')
def redirection():
    redirectUrl = meli.auth_url(redirect_URI="https://auto-delivery-totomi.c9.io/authorize")
    return redirectUrl
   # return redirect(redirectUrl, code=302)
    
@app.route('/authorize')
def authorization():
    usercode=request.args.get('code')
    meli.authorize(code=usercode, redirect_URI="https://auto-delivery-totomi.c9.io/authorize")
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
    return meli.access_token+' fifififi '+ meli.refresh_token



@app.route('/debug')
def debug():
    flash(counter)
    return 'ok'

@app.route('/')
def hello():
    return 'Hello World'

app.debug= True
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))


while meli.refresh_token:
    counter= counter +1
    time.sleep(1)
    
    