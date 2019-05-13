import pymongo
import os
import json, logging

class Mongo():
    '''
    Make Mongo connection instance
    '''
    __instance = None

    def __init__(self):
        self.mdb_client = pymongo.MongoClient('mongo', 27017)
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
            logging.debug('Json Data Added')
        else:
            logging.debug('{} is not exist'.format(jsonSourceFile))
        

    def output(self, outputpath, dbName, collectionName, includeObjID = False):
        mongoInstance = Mongo.getInstance()
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        jsonOutput = []
        dataCount = 0
        if includeObjID == True:
            for i in collection.find():
                jsonOutput.append(i)
                dataCount += 1
        else:
            for i in collection.find({}, {'_id': False}):
                jsonOutput.append(i)
                dataCount += 1
        with open(outputpath, mode = 'w') as jf:
            jf.write(json.dumps(jsonOutput, indent=4))
        logging.debug(dataCount, " have been output")
    
    def clean(self, dbName, collectionName):
        mongoInstance = Mongo.getInstance()
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        result = collection.delete_many({})
        logging.debug(result.deleted_count, " deleted.")
        