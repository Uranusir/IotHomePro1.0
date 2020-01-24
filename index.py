from flask import Flask
app = Flask(__name__)

from flask import Flask, escape, request
from jinja2 import Template
#import serInterface

def do_the_login():
    return 'login'

def show_the_login_form():
    return 'login FORM'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/user/<username>')
def show_sur_profile(username):
    return 'User %s' % escape(username)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

if __name__ == '__main__':
    app.run(debug = True)