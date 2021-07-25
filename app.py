from flask import Flask, render_template, redirect, session, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = MongoClient('mongodb://localhost:27017/')

db = client.userAccountSystemDatabase
userCollection = db.users

@app.route('/')
def index():
    if 'isLoggedIn' in session:
        return render_template('index.html', user=session['user'])
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        accountDetails = {}

        accountDetails['password'] = request.form['password'].strip()
        accountDetails['username'] = request.form['username'].strip()

        user = userCollection.find_one({'username': accountDetails['username'],'hashedPassword': accountDetails['password']})
        if user:
            # successful log in
            session['isLoggedIn'] = True
            session['user'] = {
                'userName': user['username'],
                'name': user['name']
            }
            return redirect('/')
        else:
            return jsonify({'error': 'Login Details incorrect. Please try again'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template('createAccount.html')
    else:
        accountDetails = request.form

        userDetails = {
            'name': accountDetails['name'],
            'username': accountDetails['username'],
            'hashedPassword': accountDetails['password']
        }
        userCollection.insert_one(userDetails)
        return redirect('/login')

@app.route('/delete')
def deleteDatabase():
    client.drop_database('userAccountSystemDatabase')
    return 'Deleted Databse'