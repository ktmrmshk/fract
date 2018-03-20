import json

class FractTest(object):
    HASSERT='hassert'
    HDIFF='hdiff'
    def __init__(self):
        self.query=dict()
    
    def get_template(self, TestType):
        if TestType == FractTest.HASSERT:
            self.query = self._template_hassert()
        elif TestType == FractTest.HDIFF:
            self.query = self._template_hdiff()
        else:
            pass

    def _template_hassert(self):
        query=dict()
        query['TestType'] = FractTest.HASSERT
        
        req = dict()
        req['Ghost'] = 'www.akamai.com'
        req['Method'] = 'GET'
        req['Url'] = 'https://www.akamai.com/us/en/'
        req['Header'] = {'Cookie' : 'abc=123', 'Accept-Encoding': 'gzip'}
        query['Request'] = req
        
        testcase = list()
        testcase.append( {'status_code': {'type': 'regex', 'query': '(200|404)'}} )
        testcase.append( {'Content-Type': {'type': 'regex', 'query': 'text\/html'}} )
        query['TestCase'] = testcase
        return query

    def _template_hdiff(self):
        query=dict()
        query['TestType'] = FractTest.HDIFF
        
        req = dict()
        req['Ghost'] = 'www.akamai.com'
        req['Method'] = 'GET'
        req['Url'] = 'https://www.akamai.com/us/en/'
        req['Header'] = {'Cookie' : 'abc=123', 'Accept-Encoding': 'gzip'}
        query['RequestA'] = req

        req = dict()
        req['Ghost'] = 'www.akamai.com.edgekey-staging.net'
        req['Method'] = 'GET'
        req['Url'] = 'https://www.akamai.com/us/en/'
        req['Header'] = {'Cookie' : 'abc=123', 'Accept-Encoding': 'gzip'}
        query['RequestB'] = req

        query['VarifyHeader'] = ['Last-Modified', 'Cache-Control']
        return query

    def import_query(self, query_json):
        pass

    def inspect_query(self, query):
        pass

    def export_query(self):
        pass

    def __str__(self):
        return json.dumps(self.query)



def test_FractTest():
    f=FractTest()
    f.get_template('hassert')
    print(f)
    f.get_template('hdiff')
    print(f)



if __name__ == '__main__':
    test_FractTest()

