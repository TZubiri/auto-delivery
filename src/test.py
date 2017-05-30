import flask
import os
app = flask.Flask(__name__)
app.secret_key ="***REMOVED***"



@app.route('/login')
def redirection():
    return 'hi'

os.system(r'start chrome http:\\localhost:8080\login')
app.debug= True
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 8080)))