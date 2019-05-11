from flask import Flask, request, render_template, redirect, session
import sqlite3
import sys
import hashlib


app = Flask(__name__)
DATABASE = {}


def generate_resource_uid(name, number):
    m = hashlib.sha256()
    m.update(str(name) + str(number))
    return m.hexdigest()


def initDB():
    """
    Initialise database with default admin and user(s)
    :return:
    """
    global DATABASE

    uid0 = generate_resource_uid('Admin1', 0)

    DATABASE["users"] = {
        "Admin1": {
            "Type": "admin",
            "Password": "AdminPass",
            "Quota": int(sys.maxsize),
            "Resources": set(uid0)
        },
        "User1": {
            "Type": "user",
            "Password": "UserPass",
            "Quota": int(sys.maxsize),
            "Resources": set()
        }
    }

    DATABASE["resources"] = {
        uid0: "Admin1",
    }



@app.route('/', methods=['GET'])
def index():
    """
    Initial welcome and help, does not actually do anything
    :return:
    """
    return 'Welcome to the resource manager!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login endpoint, fields of username and password
    :return:
    """
    if request.method=='GET':
        # get info and render
        return render_template('login.html')
    else:
        # auth
        username = request.form.get('username')
        password = request.form.get('password')

        if username in DATABASE:
            if password == DATABASE[username]["Password"]:
                # success, set session
                session['name'] = username

                # get info and redirect
                return redirect(manage_resources(username))

        return "Incorrect login credentials"


@app.route('/manage', methods=['GET'])
@app.route('/manage/<name>', methods=['POST', 'DELETE'])
def manage_users(name='none'):
    """
    Endpoint for management of all users
    :param name: name of user being managed
    :return:
    """

    if request.method=='GET':
        # list users
        return render_template('users.html')

    if request.method=='POST':
        # create user
        # auth from session
        # check quota, perform task
        # redirect with get
        return redirect(manage_users(name))

    if request.method=='DELETE':
        # auth from session, deny if not admin

        # check and execute task (deletes user)

        # check if current user still valid
        if session['name'] == name:
            session.clear()
            return redirect(index)

        # else, manage own resources
        return redirect(manage_users(session['name']))


@app.route('/resources/<user>', methods=['GET'])
@app.route('/resources/<user>/<uid>', methods=['POST', 'DELETE'])
def manage_resources(user, uid=""):
    if request.method=='GET':
        # check auth from session

        # list all resources available to the user
        return render_template('resource.html', user=user)

    if request.method=='POST':
        # check auth from session

        # checks current quota and resource count

        # execute task

        return render_template('resource.html', user=user)

    if request.method=='DELETE':
        # check auth from session

        # execute task and decrement resource count

        return render_template('resource.html', user=user)


if __name__ == '__main__':
    initDB()
    # set secret for session
    app.secret_key = b'super_secret_key'

    app.run(port=8080)
