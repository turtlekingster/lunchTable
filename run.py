#!/usr/bin/python
from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
#from wtformfields.html5 import DateTimeField
#from wtforms.widgets.html5 import DateTimeInput
from wtforms.fields import TextAreaField, StringField, DecimalField, SubmitField, PasswordField, IntegerField, SelectField
from functools import wraps
import lunch
import users
app = Flask(__name__, static_url_path='')
app.secret_key = 'SHH!'

class LunchCheckoutForm(FlaskForm):
    checkout = SubmitField('Checkout')

class LunchCheckinForm(FlaskForm):
    locField = StringField('Location')
    description = TextAreaField('Description')
    rating = DecimalField('Rating', places=1)
    calories = IntegerField('Calories')
    cost = DecimalField('Cost', places=2)
    checkin = SubmitField('Checkin')

class LoginForm(FlaskForm):
    username = StringField('Name')
    password = PasswordField('Password')
    login = SubmitField('Login')

class NewUserForm(FlaskForm):
    username = StringField('Name')
    password = PasswordField('Password')
    email = StringField('Email')
    group = SelectField('Group', coerce=int)
    create = SubmitField('Create')

usrHelper = users.userHelper()
lunchHelper = lunch.lunchness()

def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        print user_id
        if user_id:
            user = usrHelper.getUser(_id = user_id)
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

    columnNames = lunchHelper.getColumnNames()
    user = usrHelper.getUser(_id=str(session['user_id']))

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
            if user.atLunch:
                print user.name + " is already at lunch!"
            else:
                print user.name + ' just checkedout'
                lunchTemp = lunch.Lunch(user_id=str(session['user_id']))
                lunchTemp.setStart()
                check = lunchHelper.insertIntoTable(lunchTemp)
                user = usrHelper.getUser(_id=str(session['user_id']))
                user.checkOut()
                usrHelper.updateUser(user)

        elif 'checkin' in request.values:
            if not user.atLunch:
                print user.name + " isn't at lunch!"
            else:
                print user.name + ' just checkedin'
                lunchTemp = lunchHelper.getUnendedLunch(str(session['user_id']))
                if(lunchTemp):
                    lunchTemp.checkIn(request.form["locField"], request.form["description"],
                        request.form["calories"], request.form["rating"], request.form["cost"])
                    lunchHelper.updateLunch(lunchTemp)
                    user.checkIn()
                    usrHelper.updateUser(user)

    elif request.method == 'GET':
        print "GET REQUEST"

    tableContents = lunchHelper.getEndedLunches()
    contents = [list(x) for x in tableContents]
    for entry in contents:
        entry[7] = usrHelper.getUser(_id=entry[7]).name


    return render_template('layout.html', table_header=t_headers, inform=checkinForm, 
            outform=checkoutForm, atLunch=user.atLunch, tableContent = contents, page_name="Lunch")

@app.route("/login", methods=['POST', 'GET'])
def login():
    loginForm = LoginForm()
    newUserForm = NewUserForm()
    loginFailed=False
    session['user_id'] = 0
    response = render_template('login.html', loginForm=loginForm,
            newUserForm=newUserForm, failed = loginFailed)

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"] 
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
            response = render_template('login.html', loginForm=loginForm,
                    newUserForm=newUserForm, failed = loginFailed)

    return response

@app.route("/users", methods=['POST','GET'])
def userTest():
    acceptableHeads = ['name','description','email','atLunch','usergroup'] #for ommiting coloumns upon display
    newUserForm = NewUserForm()
    columnNames = usrHelper.getColumnNames()
    user = usrHelper.getUser(_id=str(session['user_id']))
    admin = usrHelper.groups.getGroup(int(user.group)).priv == 0 
    #this zero is code for admin one is standard user -1 to -9 and 2 to 9 are undefined privledges

    try:
        username = request.form["username"]
        password = request.form["password"]
        print request.values
        if 'email' in request.values:
            user = usrHelper.getUser(username)
            if not user:
                group_id = request.form["group"]
                print group_id
                group = usrHelper.groups.getGroup(int(group_id))
                if group:
                    email = request.form["email"]
                    user = users.User(name=username, _hash=password, email=email, group=group._id)
                    user.hashpw()
                    usrHelper.addUser(user)
                else:
                    print "Undefined group"
            else:
                print "user already exists"
    except Exception, e:
        print e

    newUserForm.group.choices = [(group._id, group.name) for group in usrHelper.groups.getGroups()]

    #print columnNames
    t_headers = []
    acceptableBodies = []
    i = 0
    for item in columnNames:
        head = item[0]
        if head in acceptableHeads:
            t_headers.append(head)
            acceptableBodies.append(i) #track columns that will be kept
        i = i + 1

    #print t_headers

    tableContents = usrHelper.getAllUsers()
    contents = [list(x) for x in tableContents]
    for entry in contents:
        entry[6] = usrHelper.groups.getGroup(int(entry[6])).name # replace groupid with group name
       #remove unwanted column data for table
        i = 0
        j = len(entry)
        ab = acceptableBodies
        while i < j:
            #print entry
            if i not in ab:
                #print str(i) + ": " + str(entry[i])
                del entry[i]
                ab = [x - 1 for x in ab]
                j = j - 1
            i = i + 1
       #-----------------------------------#
    return render_template('layout.html', table_header=t_headers , tableContent=contents,
            isAdmin=admin, newUserForm=newUserForm, page_name="Users")


@app.route("/static/<path:filename>")
def getStatic(filename):
    print "retrieving logo"
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)


if __name__ == '__main__':
    app.run(debug=True, ssl_context=('certs/cert.pem','certs/key.pem'))
