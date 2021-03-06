import pymongo
import os
import json, logging
class Mongo():
    '''
    Make Mongo connection instance
    '''
    __instance = dict()

    def __init__(self, host, port):
        self.mdb_client = pymongo.MongoClient(host, port)
        print('Connecting Mongo...')

    @staticmethod
    def getInstance(host, port):
        key='{}.{}'.format(host, port)
        if key not in Mongo.__instance:
            Mongo.__instance[key] = Mongo(host, port)
        return Mongo.__instance[key]

class mongojson():
    def __init__(self, host, port):
        self.host=host
        self.port=port

    def input(self, jsonSourceFile, dbName, collectionName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
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
        

    def output(self, outputpath, dbName, collectionName, query={}, includeObjID = False, cleanup=True):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        jsonOutput = []
        dataCount = 0
        if includeObjID == True:
            for i in collection.find():
                jsonOutput.append(i)
                dataCount += 1
        else:
            for i in collection.find(query, {'_id': False}):
                jsonOutput.append(i)
                dataCount += 1
        with open(outputpath, mode = 'w') as jf:
            jf.write(json.dumps(jsonOutput, indent=2))
        logging.debug("{} have been output".format(dataCount))

        if cleanup:
            print('removing db tables')
            self.clean(dbName, collectionName)
    
    def clean(self, dbName, collectionName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        result = collection.delete_many({})
        logging.debug("{} deleted.".format(result.deleted_count))

    def push_many(self, dict_data_list, dbName, collectionName, serializer= lambda i:i):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        collection.insert_many( [serializer(i) for i in dict_data_list] )
    
    def push_one(self, dict_data, dbName, collectionName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        collection.insert_one(dict_data)

    def find(self, query, dbName, collectionName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]

        ret=list()
        for r in collection.find(query, {'_id': False}):
            ret.append(r)
        logging.debug(ret)
        return ret
    
    def findall(self, dbName, collectionName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]

        ret=list()
        for r in collection.find({}, {'_id': False}):
            ret.append(r)
        logging.debug(ret)
        return ret


    def count(self, query, dbName, collectionName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        collection = mongodb[collectionName]
        return collection.count_documents(query)

    def delete_db(self, dbName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        mongodb.dropDataBase()

    def delete_collection(self, dbName, collectionName):
        mongoInstance = Mongo.getInstance(self.host, self.port)
        mongodb = mongoInstance.mdb_client[dbName]
        mongodb.drop_collection(collectionName)
