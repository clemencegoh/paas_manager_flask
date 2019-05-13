from flask import Flask, request, render_template, redirect, session, Response, url_for
import sqlite3
import sys
import hashlib


app = Flask(__name__)


def generate_resource_uid(name, number):
    print('received: \nuser:{}\nnumber:{}'.format(name, number))
    m = hashlib.sha256()
    m.update((str(name) + str(number)).encode())
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
            "Resources": {uid0},
            "Created": 1,
        },
        "User1": {
            "Type": "user",
            "Password": "UserPass",
            "Quota": int(sys.maxsize),
            "Resources": set([]),
            "Created": 0,
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

        users = DATABASE["users"]

        if username in users:
            if password == users[username]["Password"]:
                # success, set session
                session['Name'] = username
                session['Type'] = users[username]['Type']

                # get info and redirect
                return redirect(url_for('manage_resources', user=username), 302)
            return Response("Incorrect Login Details", 401)

        return "Incorrect login credentials"


@app.route('/users', methods=['GET', 'POST'])
@app.route('/users/<user>', methods=['DELETE'])
def manage_users(user='none'):
    """
    Endpoint for management of all users
    :param user: name of user being managed
    :return:
    """

    global DATABASE

    if request.method=='GET':
        # list users only if person is admin
        if session['Type'] == 'admin':
            return render_template('users.html',
                                   users=DATABASE["users"])
        return Response("Not authorized", 403)

    if request.method=='POST': # create user
        username = request.form.get('name')
        password = request.form.get('password')
        usertype = request.form.get('usertype')

        # auth from session
        if session['Type'] == 'admin':
            # perform task
            DATABASE["users"][username] = {
                "Type": usertype,
                "Password": password,
                "Quota": int(sys.maxsize),
                "Resources": set([]),
                "Created": 0,
            }
            print('completed')
            print('current:', DATABASE["users"])

            # redirect with get
            return redirect(url_for('manage_users'))
        return Response("Not Authorized", 403)

    if request.method=='DELETE':
        # auth from session, deny if not admin
        if session['Type'] == 'admin':
            # check and execute task (deletes user)
            try:
                if session['name'] == user:
                    return Response('Cannot delete yourself', 401)
                del DATABASE["users"][user]
            except KeyError:
                print("{} does not exist".format(user))
            return redirect(url_for('manage_users'))
        return Response("Not Authorized", 403)


@app.route('/resources/<user>', methods=['GET', 'POST'])
@app.route('/resources/<user>/<uid>', methods=['DELETE'])
def manage_resources(user, uid=""):
    """
    :param user: user
    :param uid: unique ID of resource
    :return:
    """

    global DATABASE

    userdata = DATABASE["users"][user]
    resources = userdata["Resources"]
    quota = userdata["Quota"]
    created = userdata["Created"]

    if request.method=='GET':
        # check auth from session
        if session['Name'] == user or session['Type'] == 'admin':
            # list all resources available to the user
            if quota == int(sys.maxsize):
                quota = "Unlimited"

            return render_template('resource.html',
                                   user=user,
                                   resources=resources,
                                   used=len(resources),
                                   quota=quota)
        else:
            return Response("Not Authorized", 403)

    if request.method=='POST':
        # check auth from session
        if session['Name'] == user or session['Type'] == 'admin':
            # checks current quota and resource count
            if len(resources) < int(quota):
                # execute task
                generated = generate_resource_uid(user, created)

                userdata["Created"] += 1
                resources.add(generated)
                # redirect
                return redirect(url_for('manage_resources', user=user))
            return Response("Quota exceeded", 401)
        return Response("Not Authorized", 403)

    if request.method=='DELETE':
        # check auth from session
        if session['Name'] == user or session['Type'] == 'admin':
            # execute task
            resources.discard(uid)
            return render_template('resource.html',
                                   user=user,
                                   resources=resources,
                                   used=len(resources),
                                   quota=quota)
        return Response("Not Authorized", 403)


if __name__ == '__main__':

    DATABASE = {}
    initDB()
    # set secret for session
    app.secret_key = b'super_secret_key'

    app.run(port=8080)
