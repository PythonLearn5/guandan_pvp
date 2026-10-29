#encoding: utf8

import pymongo

class MongoDB:
    def __init__(self,user,password,dbname, host='127.0.0.1',port=27017):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.conn = pymongo.MongoClient(self.host, int(self.port),
                                        username=self.user,
                                        password=self.password,
                                        authSource=dbname)
        self.db = self.conn[dbname]

guandan_db = MongoDB(user='guandan', password='jiaojiao', dbname='guandan').db