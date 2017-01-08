import os
#from flask import Flask,redirect,request,flash
import flask
import sys
#from lib.meli import Meli
import time
import json
import testUsers
import httplib2
import oauthMonkey
import oauth2client.client
import requests


counter = 0

headers = {'Accept': 'application/json', 'User-Agent': 'MELI-PYTHON-SDK-1.0.0', 'Content-type': 'application/json'}
app = flask.Flask(__name__)
app.secret_key = '***REMOVED***'



flow = oauth2client.client.flow_from_clientsecrets(
    'client_secrets.json',
    scope="https://auth.mercadolibre.com",
    redirect_uri="http://localhost:8080/authorize")

@app.route('/login')
def redirection():
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri, code=302)
    
@app.route('/authorize')
def authorization():

    auth_code=flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    credentials.user_agent = "MELI-PYTHON-SDK-1.0.0"
    user_http = httplib2.Http()
    user_http = credentials.authorize(user_http)
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
   # authorizedwebpage = 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token
    return flask.redirect("http://localhost:8080/HelloWorld", code=302)

@app.route('/success')
def successful():


   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
    return 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token

@app.route('/debug')
def debug():
    flask.flash(counter)
    return 'ok'

@app.route('/HelloWorld')
def hello():
    params = {'access_token' : meli.access_token}
    response = http
        #get(path="/users/me", params=params)
    print (type(response.content))
    print (response.content)
    print (meli.access_token)
    UsersPersonalInfo = json.loads(response.content)
    return  'Hello, ' + UsersPersonalInfo['first_name'] + UsersPersonalInfo['last_name'] + ' Your email is: ' + UsersPersonalInfo['email']

@app.route('/SecondTest')
def SecondTest():
    params = {'access_token' : meli.access_token}
    response = meli.get(path="/questions/search?item={Item_id}", params=params)
    print (type(response.content))
    print (response.content)
    print (meli.access_token)
    UsersPersonalInfo = json.loads(response.content)
    return  'Hello, ' + UsersPersonalInfo['first_name'] + UsersPersonalInfo['last_name'] + ' Your email is: ' + UsersPersonalInfo['email']

@app.route('/CreateTestUser')
def CreateTestUser():
    TestUserDict={'site_id':'MLA'}
    TestUserJson = json.dumps(TestUserDict)
    TestUserInfoResponse = meli.post('/users/test_user',TestUserJson,{'access_token' : meli.access_token})
    TestUserInfo = TestUserInfoResponse.content
    return TestUserInfo

@app.route('/sale')
def dispatchNotification():
    r = request.args.post
    return r

app.debug= True
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 8080)))


'''
while meli.refresh_token:
    counter= counter +1
    time.sleep(1)
    print "hi"
'''