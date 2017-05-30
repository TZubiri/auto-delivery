import os
from flask import Flask,redirect,request,flash
import sys
from lib.meli import Meli
import time
import json

counter = 0
app = Flask(__name__)
app.secret_key = '***REMOVED***'

meli = Meli(client_id=3410176288430291, client_secret="***REMOVED***")
redirect_URI="http://localhost:8080/authorize"

@app.route('/userstart')
def redirection():
    redirectUrl = meli.auth_url(redirect_URI)
   # return redirectUrl
    return redirect(redirectUrl, code=302)
    
@app.route('/authorize')
def authorization():
    usercode=request.args.get('code')
    meli.authorize(usercode, redirect_URI)
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
   # authorizedwebpage = 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token
    return redirect("http://localhost:8080/HelloWorld", code=302)

@app.route('/success')
def successful():


   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
    return 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token

@app.route('/debug')
def debug():
    flash(counter)
    return 'ok'

@app.route('/HelloWorld')
def hello():
    params = {'access_token' : meli.access_token}
    response = meli.get(path="/users/me", params=params)
    print (type(response.content))
    print (response.content)
    print (meli.access_token)
    UsersPersonalInfo = json.loads(response.content)
    return  'Hello, ' + UsersPersonalInfo['first_name'] + UsersPersonalInfo['last_name'] + ' Your email is: ' + UsersPersonalInfo['email']

@app.route('/SecondTest')
def SecondTest():
    params = {'access_token' : meli.access_token}
    itemId = request.args.get('itemId')
    if itemId is None:
        return 'an item id is required'

    print (itemId)
    response = meli.get(path="/questions/search?item=" + itemId , params=params)
    print (type(response.content))
    print (response.content)
    print (meli.access_token)
    itemInfo = json.loads(response.content)
    return  'Hello, ' + response.text

@app.route('/CreateTestUser')
def CreateTestUser():
    TestUserDict={'site_id':'MLA'}
    TestUserJson = json.dumps(TestUserDict)
    TestUserInfoResponse = meli.post('/users/test_user',TestUserJson,{'access_token' : meli.access_token})
    TestUserInfo = TestUserInfoResponse.content
    return TestUserInfo

@app.route('/SaleListener')
def SaleListener():
    pass



'''
while meli.refresh_token:
    counter= counter +1
    time.sleep(1)
    print "hi"
    
    '''