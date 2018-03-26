import json, logging

class FractDset(object):
    HASSERT='hassert'
    HDIFF='hdiff'
    def __init__(self):
        self.query=dict()

    def init_template(self):
        pass

    def import_query(self, query_json):
        pass

    def valid_query(self, query):
        pass

    def export_query(self):
        pass

    def __str__(self):
        pass



class FractTest(object):
    HASSERT='hassert'
    HDIFF='hdiff'
    def __init__(self):
        self.query=dict()
    
    def init_template(self):
        self.query = { \
                'TestType': str(),\
                'Request': {'Ghost': str(), 'Method':str(), 'Url':str(), 'Headers':dict() }, \
                'TestCase': dict() }

    def init_example(self, TestType):
        if TestType == FractTest.HASSERT:
            self.query = self._example_hassert()
        elif TestType == FractTest.HDIFF:
            self.query = self._example_hdiff()
        else:
            pass

    def _example_hassert(self):

        query=dict()
        query['TestType'] = FractTest.HASSERT
        
        req = dict()
        req['Ghost'] = 'www.akamai.com'
        req['Method'] = 'GET'
        req['Url'] = 'https://www.akamai.com/us/en/'
        req['Headers'] = {'Cookie' : 'abc=123', 'Accept-Encoding': 'gzip'}
        query['Request'] = req
        
        testcase = dict()
        testcase['status_code'] = [{'type': 'regex', 'query': '(200|404)'}, {'type': 'regex', 'query': '[^403]'}] 
        testcase['Content-Type'] = [{'type': 'regex', 'query': 'text\\/html$'}] 
        query['TestCase'] = testcase
        return query

    def _example_hdiff(self):
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

    def valid_query(self, query):
        pass

    def export_query(self):
        pass

    def __str__(self):
        return json.dumps(self.query)

def test_FractTest():
    f=FractTest()
    f.init_example('hassert')
    logging.debug(f)
    f.init_example('hdiff')
    logging.debug(f)


class FractResult(object):
    HASSERT='hassert'
    HDIFF='hdiff'
    def __init__(self):
        self.query=dict()

    def init_template(self):
        pass

    def get_template(self, TestType):
        if TestType == FractResult.HASSERT:
            self.query = self._template_hassert()
        elif TestType == FractResult.HDIFF:
            self.query = self._template_hdiff()
        else:
            pass
    
    def _template_hassert(self):
        query=dict()
        query['TestType'] = FractResult.HASSERT

        query['Passed'] = True
        query['Response'] = {'status_code': 200, 'Content-Length': 1234, 'Content-Type': 'text/html'}
        query['HeaderCase'] = { 'Cache-Control': [ {'Passed': True, 'Value': 'no-store', 'testcase': {'type': 'regex', 'query': '(200|404)' } } ] }
        return query

    def _template_hdiff(self):
        query=dict()
        query['TestType'] = FractResult.HDIFF

        query['Passed'] = True
        
        query['ResponseA'] = {'status_code': 200, 'Content-Length': 1234, 'Content-Type': 'text/html'}
        query['ResponseB'] = {'status_code': 200, 'Content-Length': 4567, 'Content-Type': 'text/html'}
        query['HeaderCase'] = {'Content-Length': [False, 1234, 4567], 'status_code': [True, 200, 200]}
        
        return query

    def make(testtype):
        self.TestType

    def __str__(self):
        return json.dumps( self.query )

def test_FractResult():
    f=FractResult()
    f.get_template('hassert')
    logging.debug(f)
    f.get_template('hdiff')
    logging.debug(f)

import re, requests
class Actor(object):
    def __init__(self):
        pass

    def get(self, url, headers=None, ghost=None, ssl_verify=False):
        req_headers = dict()
        if headers is not None:
            req_headers.update( headers )

        if ghost is not None:
            match = re.search('(http|https):\/\/([^\/]+)(\/.*$|$)', url)
            assert match is not None
            host = match.group(2)
            req_url = url.replace(host, ghost)
            req_headers['host'] = host

        else:
            req_url = url

        self.r = requests.get(req_url, verify=ssl_verify)
        logging.debug(req_url)
        logging.debug(req_headers)

    def headers(self):
        return self.r.headers
    
    def resh(self, headername):
        if headername == 'status_code':
            return self.r.status_code
        return self.r.headers[ headername ]
    
    def status_code(self):
        return self.r.status_code


def test_Actor():
    a = Actor()
    a.get('https://space.ktmrmshk.com/abc/example.html?abc=123', ghost='space.ktmrmshk.com.edgekey-staging.net', headers={'Accept-Encoding': 'gzip'})
    logging.debug( a.headers() )
    logging.debug( a.status_code() )
    a.get('https://space.ktmrmshk.com/abc/example.html?abc=123')
    logging.debug( a.headers() )
    logging.debug( a.status_code() )


class Fract(object):
    def __init__(self):
        self.actor=Actor()

    def run(self):
        pass

    def _run_hassert(self, fracttest):
        url = fracttest.query['Request']['Url']
        ghost = fracttest.query['Request']['Ghost']
        headers = fracttest.query['Request']['Headers']
    
        # throw HTTP request
        self.actor.get( url, headers, ghost )
        
        # validation process
        for hdr,tlist in fracttest.query['TestCase'].items():
            logging.debug('testcase hdr={}'.format(hdr))
            
            for t in tlist:
                logging.debug('  --> test={}'.format(t))
                logging.debug('hdr value: {}: {}'.format(hdr, self.actor.resh( hdr )))
                
                assert t['type'] == 'regex'
                if t['type'] == 'regex':
                    match = re.search( t['query'], str( self.actor.resh( hdr ) ) )
                    if match is not None: # test passed
                        logging.debug('  -> test passed: testcase={}'.format(t['query']) )

                    else: # test failed
                        logging.debug('  -> test failed: testcase={}'.format(t['query']) )
                else:
                    pass


    def _run_hdiff(self, fracttest):
        pass

def test_Fract():
    fr=Fract()
    testcase=FractTest()
    testcase.init_example('hassert')
    fr._run_hassert(testcase)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_FractTest()
    test_FractResult()
    #test_Actor()
    test_Fract()

