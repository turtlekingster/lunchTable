#!/usr/bin/python
import MySQLdb

class dbhelper:
    def __init__(self, host, db, user, passwd):
        try:
            self.db = MySQLdb.connect(host, user, passwd, db)
            self.cur = self.db.cursor()
        except Exception, e:
            print "Database connection error"
            print "host:"+ host +" ,db:" + db + " ,user:"+ user
            print e

    def getTableContents(self, table, content, condition=""):
        try:
            string = "SELECT " + content + " FROM " + table
            if condition != "":
                string = string + " WHERE " + condition + ";"
            else:
                string = string + ";"
            self.cur.execute(string)
            return self.cur.fetchall()
        except Exception, e:
            print "Select query failed: " + string
            print e

    def getByValue(self, table, valueName, value):
        if type(valueName) is not str:
            raise TypeError('valueName must be a str, valueName is a '+ str(type(valueName)))
        if type(value) is not str:
            raise TypeError('value must be a str, value is a ' + str(type(value)))
        try:
            print "test"
            string = "SELECT * FROM " + table + " WHERE " + valueName + "='"+ value +"';"
            self.cur.execute(string)
            return self.cur.fetchall()
        except Exception, e:
            print "Select query failed: " + string
            print e

    def insertIntoTable(self, table, values):
        try:
            string = "INSERT INTO " + table + " VALUES " + values + ";"
            self.cur.execute(string)
            return self.cur.fetchall()
        except Exception, e:
            print "INSERT query failed"
            print e
            print string

    def insertIntoTable(self, table, valueNames, values):
        if len(valueNames) != len(values):
            raise ValueError('differing number of values and names')       
        try:
            string = "INSERT INTO " + table + " ("
            i = 0
            while i < (len(valueNames) - 1):
                string = string + valueNames[i] + ", "
                i = i + 1
            string = string + valueNames[i] + ") "

            string = string + "VALUES ("
            i = 0
            while i < (len(values) - 1):
                string = string + values[i] + ", "
                i = i + 1
            string = string + values[i] + ");"
            print string
            self.cur.execute(string)
            self.db.commit()

        except Exception, e:
            print "INSERT query failed"
            print e
            print string

    def getColumnNames(self, table):
        try:
            string ="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='" + table +"';"
            self.cur.execute(string)
            return self.cur.fetchall()
        except Exception, e:
            print e


    def updateEntry(self, table, valueNames, values):
        if(len(valueNames) != len(values)):
            raise ValueError('differing number of values and names ' + str(len(values)) + ":" + str(len(valueNames)))
        try:
            string ="UPDATE " + table + " SET "
            i = 1
            while i < (len(valueNames) - 1):
                string = string + valueNames[i] + " = " + values[i] + ", "
                i=i+1
            string = string + valueNames[i] + " = " + values[i]
            
            string = string + " WHERE " + valueNames[0] + " = " + values[0]
            self.cur.execute(string)
            self.db.commit()
            print string
        except Exception, e:
            print "UPDATE query failed"
            print e
            print string

