import pymongo
import os
import json

class Mongo():
    '''
    Make Mongo connection instance
    '''
    __instance = None

    def __init__(self):
        self.mdb_client = pymongo.MongoClient('localhost', 27017)
        print('Connecting Mongo...')

    @staticmethod
    def getInstance():
        if Mongo.__instance is None:
            Mongo.__instance = Mongo()
        return Mongo.__instance

class mongojson():
    def input(self, jsonSourceFile, dbName, collectionName):
        mongoInstance = Mongo.getInstance()
        if os.path.isfile(jsonSourceFile):
            mongodb = mongoInstance.mdb_client[dbName]
            collection = mongodb[collectionName]
            with open(jsonSourceFile, mode = 'r') as jf:
                str = jf.read()
                jsonData = []
                jsonData.extend(json.loads(str))
                collection.insert_many(jsonData)
        else:
            print('{} is not exist'.format(jsonSourceFile))
        

    def output(self, outputpath, dbName, collectionName, includeObjID = False):
        mongoInstance = Mongo.getInstance()
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        jsonOutput = []
        if includeObjID == True:
            for i in collection.find():
                jsonOutput.append(i)
        else:
            for i in collection.find({}, {'_id': False}):
                jsonOutput.append(i)
        with open(outputpath, mode = 'w') as jf:
            jf.write(json.dumps(jsonOutput, indent=4))