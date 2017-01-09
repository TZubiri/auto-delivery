import os
#from flask import Flask,redirect,request,flash
import flask
import sys
#from lib.meli import Meli
import time
import json
import testUsers
import httplib2
import oauth2client.client
import meli3
import requests


counter = 0

headers = {b'Accept': b'application/json', b'User-Agent': b'MELI-PYTHON-SDK-1.0.0', b'Content-type': b'application/json',b'Accept-Encoding': b'gzip,deflate'}
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
    flow.scope = None
    credentials = flow.step2_exchange(auth_code)
    flow.scope = "https://auth.mercadolibre.com"
    user_http = httplib2.Http()
    user_http = credentials.authorize(user_http)
    print(credentials.get_access_token(user_http))
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
   # authorizedwebpage = 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token
    return showPersonalInfo(user_http,credentials)

@app.route('/success')
def successful():
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
    return 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token

@app.route('/debug')
def debug():
    flask.flash(counter)
    return 'ok'


def showPersonalInfo(user_http: httplib2.Http,credentials) -> str:
    #response = requests.get("https://api.mercadolibre.com/users/me",params={'access_token':credentials.access_token},headers=headers)
    #content = response.content

    response,content = user_http.request("https://api.mercadolibre.com/users/me","GET")
        #get(path="/users/me", params=params)
    UsersPersonalInfo = json.loads(content)
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

import os
#os.system(r'start chrome http:\\localhost:8080\login')
app.debug='true'
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 8080)))


'''
while meli.refresh_token:
    counter= counter +1
    time.sleep(1)
    print "hi"
'''