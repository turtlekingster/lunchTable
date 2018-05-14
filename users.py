#!/usr/bin/python
from dbhelper import dbhelper
import bcrypt

class User():
    def __init__(self, _id=-1, name="", description="", _hash="", email="", atLunch = False):
        self._id = _id
        self.name = name
        self.desc = description
        self._hash = _hash
        self.email = email
        self.atLunch = atLunch

    def hashpw(self):
        self._hash = bcrypt.hashpw(self._hash.encode('utf8'), bcrypt.gensalt())

    def auth(self, password):
        htemp = bcrypt.hashpw(password.encode('utf8'), self._hash)
        print htemp + "\n" + self._hash + "\n"
        return bcrypt.checkpw(password.encode('utf8'), self._hash)

    def editDescription(self, description):
        self.description = description

    def checkOut(self):
        self.atLunch = True;
    def checkIn(self):
        self.atLunch = False;

class userHelper(dbhelper):
    def __init__(self):
        self.tableName = "users"
        self.dbName = "lunch"
        dbhelper.__init__(self,"localhost", self.dbName, "justin", "0828")

    def getUser(self, name="", email="", _id=-1):
        entry = [] 
        if(name != ""):
            entry = dbhelper.getByValue(self, self.tableName, "name", str(name))
        elif(email != ""):
            entry = dbhelper.getByValue(self, self.tableName, "email", str(email))
        elif(_id > 0):
            user_id = str(_id)
            entry = dbhelper.getByValue(self, self.tableName, "id", str(user_id))
        else:
            raise ValueError('No UserName, Email, or ID Specified')
        if entry: 
            _id = entry[0][0]
            name = entry[0][1]
            description = entry[0][2]
            _hash = entry[0][3]
            email = entry[0][4]
            atLunch = entry[0][5]
            return User(_id, name, description, _hash, email, atLunch)
        return 0

    def addUser(self, user):
        if not isinstance(user, User):
            raise TypeError('Need user type')
        elif user.name == "":
            raise ValueError('Blank Username')
        valueNames = ["name", "description", "password", "email", "atLunch"]
        values = ["'" + user.name + "'","'" + user.desc + "'","'" + user._hash + "'","'" + user.email + "'","'" + str(int(user.atLunch)) +"'"]
        dbhelper.insertIntoTable(self, "users", valueNames, values)

    def updateUser(self, user):
        if not isinstance(user, User):
            raise TypeError('Need user type')
        elif user.name == "":
            raise ValueError('Blank Username')
        try:
            valueNames = ["id", "name", "description", "password", "email", "atLunch"]
            values = ["'" + str(user._id) + "'", "'" + user.name + "'","'" + user.desc + "'","'" + user._hash + "'","'" + user.email + "'","'" + str(int(user.atLunch)) +"'"]
            print "Ollo!"
            dbhelper.updateEntry(self, "users", valueNames, values)
        except Exception, e:
            print "-------In updateUser:"
            print e


