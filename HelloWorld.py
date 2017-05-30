import os
from flask import Flask,redirect,request,flash,url_for
import sys
from lib.meli import Meli
import time
import json

counter = 0
app = Flask(__name__)
print(os.environ)
app.secret_key = os.getenv('secret_key')
meli = Meli(client_id=os.getenv('client_id'), client_secret=os.getenv("client_secret"))
base_uri = os.getenv('base_uri')
redirect_uri= base_uri + "/authorize"
app.config['SERVER_NAME'] = base_uri
@app.route('/userstart')
def redirection():
    authed_redirect_uri = meli.auth_url(redirect_uri)
   # return redirectUrl
    return redirect(authed_redirect_uri, code=302)
    
@app.route('/authorize')
def authorization():
    usercode=request.args.get('code')
    meli.authorize(usercode, redirect_URI)
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
   # authorizedwebpage = 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token
    return redirect(url_for("/HelloWorld"), code=302)

@app.route('/success')
def successful():
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
    return 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token

@app.route('/HelloWorld')
def hello():
    params = {'access_token' : meli.access_token}
    response = meli.get(path="/users/me", params=params)
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

@app.route('/callbacks')
def callbacksHandler():

    postParams = json.loads(request.args.post())
    print
    topic = postParams['topic']
    topic_to_function = {'items': item_handler,
                         'orders': orders_handler,
                         'questions': questions_handler,
                         'payments': payments_handler
                         }
    handler = topic_to_function.get(topic,None)
    handler(postParams)

def payments_handler(**kwargs):
    kwargs['resource']