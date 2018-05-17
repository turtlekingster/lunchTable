#!/usr/bin/python
from dbhelper import dbhelper
import bcrypt

class User():
    def __init__(self, _id=-1, name="", description="", _hash="", email="", atLunch = False, group = -1):
        self._id = _id
        self.name = name
        self.desc = description
        self._hash = _hash
        self.email = email
        self.atLunch = atLunch
        self.group = group

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

class Group():
    def __init__(self, _id=-1, name="", priv=9):
        self._id = _id
        self.name = name
        self.priv = priv

class groupHelper(dbhelper):
    def __init__(self):
        self.tableName = "usergroups"
        self.dbName = "lunch"
        dbhelper.__init__(self,"localhost", self.dbName, "justin", "0828")
        self.lastID = 0
        self.getGroups()

    def getGroups(self):
        entries = dbhelper.getTableContents(self, self.tableName, "*")
        self.groups = []
        for entry in entries:
            self.groups.append(Group(entry[0], entry[1], entry[2]))
        self.lastID = self.groups[len(self.groups) - 1]._id

    def addGroup(self, name="", priv=9):
        self.lastID = self.lastID + 1
        group = Group(self.lastID, name, priv)
        valueNames = ["id","name","priv"]
        values = ["'" + group._id + "'", "'" + group.name + "'", "'" + group.priv + "'"]
        dbhelper.insertIntoTable(self, self.tableNames, valueNames, values)
        self.getGroups(self)

    def getGroup(self, _id = -1, name = ""):
        if(_id != -1):
            return self.groups[_id]
        elif(name != ""):
            for group in self.groups:
                if group.name == name:
                    return group
        return 0
        
    def __del__(self):
        dbhelper.__del__(self)

class userHelper(dbhelper):
    def __init__(self):
        self.tableName = "users"
        self.dbName = "lunch"
        dbhelper.__init__(self,"localhost", self.dbName, "justin", "0828")
        self.groups = groupHelper()

    def getAllUsers(self):
        return dbhelper.getTableContents(self, self.tableName, "*")

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
            group_id= entry[0][6]

            return User(_id, name, description, _hash, email, atLunch, group_id)
        return 0

    def addUser(self, user):
        if not isinstance(user, User):
            raise TypeError('Need user type')
        elif user.name == "":
            raise ValueError('Blank Username')
        valueNames = ["name", "description", "password", "email", "atLunch", "usergroup"]
        values = ["'" + user.name + "'","'" + user.desc + "'","'" + user._hash + "'",
                "'" + user.email + "'","'" + str(int(user.atLunch)) +"'", "'" + str(user.group) + "'"]
        dbhelper.insertIntoTable(self, self.tableName, valueNames, values)

    def updateUser(self, user):
        if not isinstance(user, User):
            raise TypeError('Need user type')
        elif user.name == "":
            raise ValueError('Blank Username')
        try:
            valueNames = ["id", "name", "description", "password", "email", "atLunch", "usergroup"]
            values = ["'" + str(user._id) + "'", "'" + user.name + "'","'" + user.desc + "'",
                    "'" + user._hash + "'","'" + user.email + "'","'" + str(int(user.atLunch)) +"'", "'" + str(user.group) + "'"]
            dbhelper.updateEntry(self, self.tableName, valueNames, values)
        except Exception, e:
            print "-------In updateUser:"
            print e

    def getColumnNames(self):
        return dbhelper.getColumnNames(self, self.tableName)

    def __del__(self):
        dbhelper.__del__(self)
