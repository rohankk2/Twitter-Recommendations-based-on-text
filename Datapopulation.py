import sqlite3
import json
from collections import namedtuple
from sqlite3 import Error
from Constants.Columns import ColumnConstants
from db.dbFactory import dbFactory

def populateTableFromJson(tableName,jsonData):
    colConstants = ColumnConstants()
    mapping = colConstants.getColumnMapping(tableName)
    dictmapping = colConstants.getColumnDict(tableName)

    sql = ''' INSERT OR IGNORE INTO ''' + tableName + '''('''
    mappingstring = ",".join(mapping)
    sql = sql + mappingstring + ''') VALUES('''
    properties =[]
    i = len(mapping)
    for prop in mapping:
        if (prop in dictmapping):
            properties.append(jsonData[dictmapping[prop]])
        else:
            properties.append(jsonData[prop])
        sql = sql + '''?'''
        if(i != 1):
            sql = sql+','
        i=i-1
    sql = sql + ')'
    obj = tuple(properties)
    factory = dbFactory()
    factory.set_connection()
    cur = factory.get_connection().cursor()
    cur.execute(sql,obj)
    factory.get_connection().commit()
    return cur.lastrowid


with open("data/users.json") as f:
    data = json.load(f)
    for user in data:
        populateTableFromJson('userTable',user)
with open("data/tweets.json") as f:
    data = json.load(f)
    for tweet in data:
        populateTableFromJson('processedTweets',tweet)



