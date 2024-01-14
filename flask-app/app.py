from pymongo import MongoClient
import os

import flask
from flask import jsonify, render_template, request, redirect, url_for, flash

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, login_required, current_user
# from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# from json import dumps, loads

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
            return redirect(url_for('profile'))
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


@app.route('/profile', methods=['GET'])
@login_required
def profile():

    my_books = database.books.find({"current_occupant_username": current_user.username, "status": "loaned"})
    my_reservations = database.books.find({"current_occupant_username": current_user.username, "status": "reserved"})
    my_fines = database.fines.find({"username": current_user.username})
    # total_fine = 0
    # for fine in my_fines:
        # total_fine += fine['amount']
    return render_template(
        'profile.html',
        user=current_user,
        my_books=list(my_books),
        my_reservations=list(my_reservations),
        my_fines=list(my_fines)
    )

@app.route('/')
def index():
    return render_template('index.html', user=current_user)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        
        # log from keys 
        app.logger.info(request.form.keys())
        
        query = request.form['query']
        results = database.users.find({"$text": {"$search": query}})
        return render_template('search.html', search_results=results)
    return render_template('search.html')


@app.route('/deposit_money', methods=['GET', 'POST'])
@login_required
def deposit_money():
    if request.method == 'POST':
        amount = int(request.form['amount'])
        database.users.update_one({"username": current_user.username}, {"$inc": {"current_balance": amount}})
        return redirect(url_for('profile'))
    return render_template('deposit_money.html', user=current_user)


@app.route('/withdraw_money', methods=['GET', 'POST'])
@login_required
def withdraw_money():
    if request.method == 'POST':
        amount = int(request.form['amount'])

        if amount < 0:
            return render_template('withdraw_money.html', user=current_user, error='Invalid amount')

        if amount > current_user.current_balance:
            return render_template('withdraw_money.html', user=current_user, error='Not enough money')

        
        database.users.update_one({"username": current_user.username}, {"$inc": {"current_balance": -amount}})
        return redirect(url_for('profile'))
    return render_template('withdraw_money.html', user=current_user)


@app.route('/user/<username>', methods=['GET'])
def user(username):
    user = database.users.find_one({"username": username})
    if not user:
        return render_template('404.html', user=current_user)
    return render_template('user.html', data=user, user=current_user)

@app.route('/book/<isbn>', methods=['GET'])
def book(isbn):
    book = database.books.find_one({"isbn": isbn})
    if not book:
        return render_template('404.html', user=current_user)
    return render_template('book.html', data=book, user=current_user)

@app.route('/reservation/<isbn>/cancel', methods=['GET'])
@login_required
def cancel_reservation(isbn):
    book = database.books.find_one({"isbn": isbn})
    if not book:
        return render_template('404.html', user=current_user)
    if book['status'] != 'reserved':
        return render_template('404.html', user=current_user)

    reservation_deadline = book['deadline'] # example value: "2023-03-23"
    reservation_deadline = datetime.datetime.strptime(reservation_deadline, '%Y-%m-%d') # convert to datetime object
    # if reservation deadline is passed then fine the user for 10 liras for each day
    datetime_delta = reservation_deadline - datetime.datetime.now()

    if datetime_delta.days < 0:
        database.fines.insert_one({"username": current_user.username, "amount": -datetime_delta.days * 10})

    database.books.update_one({"isbn": isbn}, {"$set": {"status": "available", "current_occupant_username": None}})
    return redirect(url_for('profile'))

@app.route('/book/<isbn>/reserve', methods=['GET'])
@login_required
def reserve_book(isbn):
    book = database.books.find_one({"isbn": isbn})
    if not book:
        return render_template('404.html', user=current_user)
    if book['status'] != 'available':
        return render_template('404.html', user=current_user)
    database.books.update_one({"isbn": isbn}, {"$set": {"status": "reserved", "current_occupant_username": current_user.username}})
    return redirect(url_for('profile'))

@app.route('/book/<isbn>/loan', methods=['GET'])
@login_required
def loan_book(isbn):
    book = database.books.find_one({"isbn": isbn})
    if not book:
        return render_template('404.html', user=current_user)
    if book['status'] != 'reserved':
        return render_template('404.html', user=current_user)
    database.books.update_one({"isbn": isbn}, {"$set": {"status": "loaned", "current_occupant_username": current_user.username}})
    return redirect(url_for('profile'))

@app.route('/book/<isbn>/return', methods=['GET'])
@login_required
def return_book(isbn):
    book = database.books.find_one({"isbn": isbn})
    if not book:
        return render_template('404.html', user=current_user)
    if book['status'] != 'loaned':
        return render_template('404.html', user=current_user)
    database.books.update_one({"isbn": isbn}, {"$set": {"status": "available", "current_occupant_username": None}})
    return redirect(url_for('profile'))

@app.route('/fine/<int:fine_id>/pay', methods=['GET'])
@login_required
def pay_fine(fine_id):
    fine = database.fines.find_one({"fine_id": fine_id})
    if not fine:
        return render_template('404.html', user=current_user)
    
    if fine['fine_amount'] > current_user.current_balance:
        return render_template('profile.html', user=current_user, error='Not enough money')

    # delete fine
    database.fines.delete_one({"fine_id": fine_id})
    # deduct money from user
    database.users.update_one({"username": current_user.username}, {"$inc": {"current_balance": -fine['fine_amount']}})

    return redirect(url_for('profile'))


# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)