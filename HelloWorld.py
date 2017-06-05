import os
from flask import Flask,redirect,request,flash,url_for,render_template,jsonify
from flask_login import LoginManager,login_user,login_required,current_user
import sys
from lib.meli import Meli
import time
import json
from AutodeliveryUser import User

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')
login_manager = LoginManager()
login_manager.init_app(app)
base_uri = os.getenv('base_uri')
redirect_uri= base_uri + "/authorize"

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login')
def redirection():
    meli = Meli(client_id=os.getenv('client_id'), client_secret=os.getenv("client_secret"))
    authed_redirect_uri = meli.auth_url(redirect_uri)
    #return redirectUrl
    return redirect(authed_redirect_uri, code=302)
    
@app.route('/authorize')
def authorization():
    usercode=request.args.get('code')
    meli = Meli(client_id=os.getenv('client_id'), client_secret=os.getenv("client_secret"))
    meli.authorize(usercode, redirect_uri)
    params = {'access_token' : meli.access_token}
    r = meli.get(path="/users/me", params=params)
    if r.status_code == 200:
        user = User(r.json()['id'],meli.access_token,meli.refresh_token)
        login_user(user)
    else:
        #TODO: Log error. Show support contact info.
        return 'Could not login correctly. Please contact support'
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
   # authorizedwebpage = 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token
    return redirect(base_uri + "/test", code=302)

@app.route('/success')
def successful():
   # params = {'access_token' : meli.access_token}
   # response = meli.get(path="/users/5000", params=params)
    return 'successful.  Access Token: ' + meli.access_token+' Refresh Token: '+ meli.refresh_token

@app.route('/test')
@login_required
def hello():
    params = {'access_token' : current_user.access_token}
    meli = Meli(client_id=os.getenv('client_id'), client_secret=os.getenv("client_secret"))
    meli.refresh_token = current_user.refresh_token
    meli.access_token = current_user.access_token
    response = meli.get(path="/users/me", params=params)
    UsersPersonalInfo = json.loads(response.content)
    return  UsersPersonalInfo['first_name'] + UsersPersonalInfo['last_name']

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

@app.route('/Stock')
@login_required
def manageStock():
    print(current_user.get_id())
    return render_template('StockManage.html')

@app.route('/StockList',methods=['POST'])
@login_required
def stockList():
    response = {}
    response["Result"] = "OK"
    response["Records"] = []
    for stock in current_user.stock_list():
        response["Records"].append({
            "stockID":str(stock.id),
            "resource":stock.resource,
            "item_name":stock.item_name
        })
    return jsonify(response)

@app.route('/updateStock')
@login_required
def updateStock():
    current_user.get_id()
    print(request.args['resource'])

@app.route('/callbacks')
def callbacksHandler():
    if request.args['topic'] == 'items':
        payments_handler(request.args['resource'],request.args['user_id'],request.args['application_id'])
    if request.args['topic'] == 'questions':
        questions_handler(request.args['resource'],request.args['user_id'])
    if request.args['topic'] == 'orders':
        orders_handler(request.args['resource'],request.args['user_id'])
    return '200'


def payments_handler(resource:str,user_id:str, application_id:str):
    pass
def orders_handler(resource:str, user_id:str):
    pass
def questions_handler(resource:str,user_id:str):
    pass