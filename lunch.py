#!/usr/bin/python
import MySQLdb
from dbhelper import dbhelper
from datetime import datetime

class Lunch(object):
    def __init__(self, _id=-1, start=datetime.fromordinal(693596).strftime('%Y-%m-%d %H:%M:%S'), 
            end=datetime.fromordinal(693596).strftime('%Y-%m-%d %H:%M:%S'), 
            location="", description="", calories=0, rating=0.0, user_id=-1, cost=0.0):
        self._id = _id
        self.start = start
        self.end = end
        self.location = location
        self.desc = description
        self.calories = calories
        self.rating = rating
        self.user_id = user_id
        self.cost = cost
    def setEnd(self):
        self.end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def setStart(self):
        self.start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def checkIn(self, location="", description="", calories=0, rating=0.0, cost=0.0):
        self.location = location
        self.desc = description
        self.calories = calories
        self.rating = rating
        self.cost = cost
        self.setEnd()

class lunchness(dbhelper):
    def __init__(self):
        self.tableName = "lunch"
        self.dbName = self.tableName
        dbhelper.__init__(self, "localhost", self.dbName, "justin", "0828")

    def getUserLunches(self, user_id):
        return self.getTableContents("user='" + str(user_id) + "' and start > end")
    def getEndedLunches(self):
        return self.getTableContents("start < end")
    def getTableContents(self, condition=""):
        return dbhelper.getTableContents(self, self.tableName, "*", condition)

    def getColumnNames(self):
        return dbhelper.getColumnNames(self, self.tableName)

    def insertIntoTable(self, lunch):
        if not isinstance(lunch, Lunch):
            raise TypeError('Need ' + str(Lunch)+ ' type. Got a ' +  str(type(lunch)))
        valueNames = ["start","end","location","description","calories","rating","user_id","cost"]
        values = ["'"+lunch.start +"'","'"+lunch.end +"'","'"+lunch.location +"'",
                "'"+lunch.desc +"'","'"+str(lunch.calories) +"'","'"+str(lunch.rating) +"'",
                "'"+str(lunch.user_id) +"'","'"+str(lunch.cost) +"'"]
        return dbhelper.insertIntoTable(self, self.tableName, valueNames, values)
    
    def updateLunch(self, lunch):
        if not isinstance(lunch, Lunch):
            raise TypeError('Need ' + str(Lunch)+ ' type. Got a ' +  str(type(lunch)))
        valueNames = ["id","start","end","location","description","calories","rating","user_id","cost"]
        values = ["'"+ str(lunch._id) +"'","'"+lunch.start +"'","'"+lunch.end +"'",
                "'"+lunch.location +"'","'"+lunch.desc +"'","'"+str(lunch.calories) +"'",
                "'"+str(lunch.rating) +"'","'"+str(lunch.user_id) +"'","'"+str(lunch.cost) +"'"]
       
        return dbhelper.updateEntry(self, self.tableName, valueNames, values)

    def getUnendedLunch(self, _id):
        entry = []
        string = "user_id = '" + _id + "' and start > end "
        entry = dbhelper.getTableContents(self, self.tableName, "*", string)
        if entry:
            _id = entry[0][0]
            start = entry[0][1].strftime('%Y-%m-%d %H:%M:%S')
            end = entry[0][2]
            location = entry[0][3]
            description = entry[0][4]
            calories = entry[0][5]
            rating = entry[0][6]
            user_id = entry[0][7]
            cost = entry[0][8]
            return Lunch(_id, start, end, location, description, calories, rating, user_id, cost)
        return 0

    def __del__(self):
        dbhelper.__del__(self)
