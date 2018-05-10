#!/usr/bin/python
import MySQLdb
from dbhelper import dbhelper

class lunchness(dbhelper):
    def __init__(self):
        self.tableName = "lunch"
        self.dbName = self.tableName
        dbhelper.__init__(self, "localhost", self.dbName, "justin", "0828")

    def getTableContents(self):
        return dbhelper.getTableContents(self, self.tableName, "*")

    def getColumnNames(self):
        return dbhelper.getColumnNames(self, self.tableName)

    def insertIntoTable(self, start, end, location, description, rating):
        string = "( '" + start + "', '" + end + "', '" + location + "', '" + description + "', " + rating + ")"
        return dbhelper.insertIntoTable(self, self.tableName, string)
    
    def checkOut(self, start, user_id):
        return dbhelper.insertIntoTable(self, self.tableName, ["start", "user_id"], ["'" + start + "'", "'"+ str(user_id) + "'"])
