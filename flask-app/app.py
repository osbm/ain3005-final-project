from pymongo import MongoClient
import os

import flask
from flask import jsonify, render_template, request, redirect, url_for, flash

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
# from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


mongo_uri = os.environ.get('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
database = mongo_client.las


login_manager = LoginManager()
app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
jwt = JWTManager(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # get username and password from the request
        username = request.form['username']
        password = request.form['password']
    
        # check if the username and password are correct
        # check if username exists in database
        user = database.users.find_one({'username': username})
        if not user:
            return render_template('index.html', error='Username not found')
    
        # check if password is correct
        if password != user['password']:
            return render_template('index.html', error='Incorrect password')
    
        # create the access token
        access_token = create_access_token(identity=username)
        return redirect(url_for('protected', access_token=access_token))


# login with JWT
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # get username and password from the request
    username = request.form['username']
    password = request.form['password']

    # check if the username and password are correct
    # check if username exists in database
    user = database.users.find_one({'username': username})
    if not user:
        return render_template('login.html', error='Username not found')

    # check if password is correct
    if password != user['password']:
        return render_template('login.html', error='Incorrect password')

    # create the access token
    access_token = create_access_token(identity=username)
    return redirect(url_for('protected', access_token=access_token))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    # get username and password from the request
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['user_type']
    birthday = request.form['birthday']
    email = request.form['email']
    
    # check if the username, or email already exists in database
    user = database.users.find_one({'username': username})
    # if user:
    #     return render_template('signup.html', form=request.form, error='Username already exists')
    # user = database.users.find_one({'email': email})
    # if user:
    #     return render_template('signup.html', error='Email already exists')
    
    # create the new user
    database.users.insert_one(
        {
            'name': name,
            'surname': surname,
            'username': username,
            'password': password,
            'user_type': user_type,
            'birthday': birthday,
            'email': email
        }
    )
    
    # create the access token
    access_token = create_access_token(identity=username)
    return redirect(url_for('protected', access_token=access_token))
    
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return render_template('protected.html', user=current_user)
    


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


# delete account
@app.route('/delete', methods=['GET', 'POST'])
# @jwt_required
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    
    # get username and password from the request
    username = request.form['username']
    password = request.form['password']
    
    # check if the username and password are correct
    # check if username exists in database
    user = database.users.find_one({'username': username})
    if not user:
        return render_template('delete.html', error='Username not found')
    
    # check if password is correct
    if password != user['password']:
        return render_template('delete.html', error='Incorrect password')
    
    # delete the user
    database.users.delete_one({'username': username})
    return redirect(url_for('logout'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)