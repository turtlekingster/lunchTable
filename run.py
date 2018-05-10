#!/usr/bin/python
from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateTimeField
from wtforms.widgets.html5 import DateTimeInput
from wtforms.fields import TextAreaField, StringField, DecimalField, SubmitField, PasswordField
from datetime import datetime
from functools import wraps
import lunch
import users
app = Flask(__name__, static_url_path='')
app.secret_key = 'SHH!'

class ExampleForm(FlaskForm):
    dateTimeWidget = DateTimeInput()
    startField = DateTimeField('DateTimePicker', format='%Y-%m-%d %H:%M:%S', widget=dateTimeWidget)
    endField = DateTimeField('DateTimePicker', format='%Y-%m-%d %H:%M:%S')
    locField =  StringField('Location')
    description = TextAreaField('Description')
    rating = DecimalField('Rating', places=1)

class LunchCheckoutForm(FlaskForm):
    checkout = SubmitField('Checkout')


class LunchCheckinForm(FlaskForm):
    locField = StringField('Location')
    description = TextAreaField('Description')
    rating = DecimalField('Rating', places=1)
    checkin = SubmitField('Checkin')

class LoginForm(FlaskForm):
    username = StringField('Name')
    password = PasswordField('Password')
    login = SubmitField('Login')

class NewUserForm(FlaskForm):
    username = StringField('Name')
    password = PasswordField('Password')
    email = StringField('Email')
    create = SubmitField('Create')


def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        userHelper = users.userHelper()
        user_id = session.get('user_id')
        print user_id
        if user_id:
            user = userHelper.getUser(_id = user_id)
            if user:
                # Success!
                return function_to_protect(*args, **kwargs)
            else:
                flash("Session exists, but user does not exist (anymore)")
                return redirect(url_for('login'))
        else:
            flash("Please log in")
            return redirect(url_for('login'))

    return wrapper


@app.route("/main", methods=['POST', 'GET'])
@login_required
def main():
    
    lunchHelper = lunch.lunchness()
    tableContents = lunchHelper.getTableContents()
    columnNames = lunchHelper.getColumnNames()

    t_headers = []
    for item in columnNames:
        head = item[0]
        t_headers.append(head)

    checkinForm = LunchCheckinForm()
    checkoutForm = LunchCheckoutForm()
    if checkinForm.validate_on_submit():
        print "WORKS!!"

    if checkoutForm.validate_on_submit():
        print "WORKS!!"

    if request.method == 'POST':
        print "POST REQUEST"
        #print request.values
        if 'checkout' in request.values:
            print 'checkout'
            outTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            check = lunchHelper.checkOut(outTime, session['user_id'])
            print check

        elif 'checkin' in request.values:
            print 'checkin'
            inTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    elif request.method == 'GET':
        print "GET REQUEST"

    return render_template('template.html', table_header=t_headers, inform=checkinForm, outform=checkoutForm)

@app.route("/login", methods=['POST', 'GET'])
def login():
    usrHelper = users.userHelper()
    loginForm = LoginForm()
    newUserForm = NewUserForm()
    loginFailed=False
    response = render_template('login.html', loginForm=loginForm, newUserForm=newUserForm, failed = loginFailed)

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if 'email' in request.values:
            user = usrHelper.getUser(username)
            if not user:
                email = request.form["email"]
                user = users.user(name=username, _hash=password, email=email)
                user.hashpw()
                usrHelper.addUser(user)
            else:
                print "user already exists"
        else:
            user = usrHelper.getUser(str(username))
            if not user:
                loginFailed = True
                print "invalid username"
            elif(user.auth(password)):
                print "valid password"
                response = redirect(url_for("main"))
                session['user_id'] = user._id
                print session.get('user_id')
            else:
                loginFailed = True
                print "invalid password"
            if loginFailed:
                response = render_template('login.html', loginForm=loginForm, newUserForm=newUserForm, failed = loginFailed)

    return response

@app.route("/users", methods=['POST','GET'])
def userTest():
    usrHelper = users.userHelper()
    usrHelper.getUser("test")

@app.route("/static/<path:filename>")
def getStatic(filename):
    print "retrieving logo"
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)


if __name__ == '__main__':
    app.run(debug=True)
