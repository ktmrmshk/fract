import pymongo

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
    def input(self, jsonsource):
        pass

    def output(self, outputpath):
        pass
    
