from pymongo import MongoClient
import os

import flask
from flask import jsonify, render_template, request, redirect, url_for, flash

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, login_required, current_user
# from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


mongo_uri = os.environ.get('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
database = mongo_client.las


login_manager = LoginManager()
app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
jwt = JWTManager(app)


class User(UserMixin):
    def __init__(self, username=None, password=None, user_type=None, birthdate=None, email=None, name=None, surname=None, current_balance=None, active=True, id=None, **kwargs):
        self.id = username

        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = birthdate
        self.user_type = user_type
        self.current_balance = current_balance

        self.username = username
        self.password = password
        self.active = active



    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    

@login_manager.user_loader
def load_user(user_id):
    user = database.users.find_one({"username": user_id})
    if not user:
        return None
    return User(**user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = database.users.find_one({"username": request.form['username']})
        if user and request.form['password'] == user['password']:
            user_obj = User(**user)
            login_user(user_obj)
            return redirect(url_for('protected'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = database.users.find_one({"username": request.form['username']})
        if user:
            return render_template('signup.html', error='Username already exists')
        database.users.insert_one({"username": request.form['username'], "password": request.form['password']})
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return render_template('protected.html', user=current_user)

@app.route('/')
def index():
    return render_template('index.html', user=current_user)

if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)