import json, logging

'''
Backlog:

* negative regex match support
* base class of FactDset
* start with, end with, contain, doesnot, equal function
* example json with text not code
* using class to define each TestType Structures

* testcode
* 
'''


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
        query_json='''{"TestType":"hassert","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text\\/html$"}]}}'''
        return json.loads( query_json )

    def _example_hdiff(self):
        query_json='''{"TestType":"hdiff","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeader":["Last-Modified","Cache-Control"]}'''
        return json.loads( query_json )
        
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
        self.query={'TestType':str(),\
                'Passed' : bool(),\
                'Response': {'status_code':int()},\
                'ResultCase': dict()}

    def init_template(self, TestType):
        pass

    def get_template(self, TestType):
        if TestType == FractResult.HASSERT:
            self.query = self._template_hassert()
        elif TestType == FractResult.HDIFF:
            self.query = self._template_hdiff()
        else:
            pass
    
    def _template_hassert(self):
        query_json='''{"TestType":"hassert","Passed":false,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":false,"Value":301,"testcase":{"type":"regex","query":"(200|404)"}},{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":false,"Value":"This Header is not in Response","testcase":{"type":"regex","query":"text/html$"}}]}}'''
        return json.loads( query_json )

    def _template_hdiff(self):
        query=dict()
        query['TestType'] = FractResult.HDIFF

        query['Passed'] = True
        
        query['ResponseA'] = {'status_code': 200, 'Content-Length': 1234, 'Content-Type': 'text/html'}
        query['ResponseB'] = {'status_code': 200, 'Content-Length': 4567, 'Content-Type': 'text/html'}
        query['ResultCase'] = {'Content-Length': [False, 1234, 4567], 'status_code': [True, 200, 200]}
        query['ResultCase'] = {'Content-Length': [False, 1234, 4567], 'status_code': [True, 200, 200]}
        
        return query

    def setTestType(self, TestType):
        assert TestType == FractResult.HASSERT or TestType == FractResult.HDIFF
        self.query['TestType'] = TestType

    def setPassed(self, passed):
        assert type(passed) == type(bool())
        self.query['Passed'] = passed

    def setResponse(self, status_code, response_headers):
        res = dict()
        res['status_code'] = status_code
        for k,v in response_headers.items():
            res[k] = v
        self.query['Response'] = res
        logging.debug('response: {}'.format(self.query['Response']))

    def setResultCase(self, hdrname, passed, val, testcase):
        self.query[Header]

    def setPassed(self, passed):
        self.query['Passed'] = passed

    def check_passed(self):
        '''
        return: (bool) passed, (int) cnt_testcase, (int) cnt_passed, (int) not_passed
        '''
        cnt_test=0
        cnt_passed=0
        cnt_failed=0
        passed=bool()
        for hdr,res in self.query['ResultCase'].items():
            for t in res:
                cnt_test+=1
                if t['Passed'] == True:
                    cnt_passed+=1
                else:
                    cnt_failed+=1
        else:
            if cnt_test == cnt_passed:
                passed=True
            else:
                passed=False

        self.query['Passed'] = passed
        return passed, cnt_test, cnt_passed, cnt_failed
    

    def __str__(self):
        return json.dumps( self.query )

def test_FractResult():
    f=FractResult()
    f.get_template('hassert')
    logging.debug(f)
    f.get_template('hdiff')
    logging.debug(f)
    f.setResponse(200, {'Content-Length': 9821, 'Content-Encoding': 'gzip'})
    


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
            logging.debug('Actor: host={}, req_url={}, req_headers = {}'.format(host, req_url, req_headers))

        else:
            req_url = url

        self.r = requests.get(req_url, headers=req_headers, verify=ssl_verify, allow_redirects=False)
        logging.debug(req_url)
        logging.debug(req_headers)

    def get_headers(self):
        hdr = self.r.headers
        hdr['status_code'] = self.r.status_code
        return hdr
    
    def resh(self, headername):
        if headername == 'status_code':
            return self.r.status_code
        return self.r.headers[ headername ]
    
    def get_status_code(self):
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
        '''
        input: FractTest object
        return: FractResult object

        '''
        res = FractResult()
        res.setTestType(FractResult.HASSERT)

        url = fracttest.query['Request']['Url']
        ghost = fracttest.query['Request']['Ghost']
        headers = fracttest.query['Request']['Headers']
    
        # throw HTTP request
        self.actor.get( url, headers, ghost )
        res.setResponse(self.actor.get_status_code(), self.actor.get_headers() )
        
        # validation process
        for hdr,tlist in fracttest.query['TestCase'].items():
            
            logging.debug('testcase hdr={}'.format(hdr))
            hdr_resultcase = list()
            has_this_header = False

            if hdr in self.actor.get_headers():
                has_this_header = True
                logging.debug('hdr value: {}: {}'.format(hdr, self.actor.resh( hdr )))
            else:
                logging.debug('hdr value: {}: Not Included on Response'.format(hdr))

            for t in tlist:
                logging.debug('  --> test={}'.format(t))
                
                assert t['type'] == 'regex'
                if has_this_header:
                    if t['type'] == 'regex':
                        match = re.search( t['query'], str( self.actor.resh( hdr ) ) )
                        if match is not None: # test passed
                            logging.debug('  -> test passed: testcase={}'.format(t['query']) )
                            hdr_resultcase.append(\
                                    {'Passed': True,\
                                    'Value':self.actor.resh( hdr ),\
                                    'testcase': t })
                        else: # test failed
                            logging.debug('  -> test failed: testcase={}'.format(t['query']) )
                            hdr_resultcase.append(\
                                    {'Passed': False,\
                                    'Value':self.actor.resh( hdr ),\
                                    'testcase': t })

                    else: # type is not regex
                        pass
                else: # header not in response
                    logging.debug('  -> test failed: testcase={}'.format(t['query']) )
                    hdr_resultcase.append(\
                            {'Passed': False,\
                            'Value':'This Header is not in Response',\
                            'testcase': t })
            res.query['ResultCase'][hdr] = hdr_resultcase            

            # check if passed at whole testcase
            psd = res.check_passed()
            logging.debug('ResultCase: {}'.format(res))
            
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

