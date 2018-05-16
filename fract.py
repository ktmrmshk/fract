import json, logging, yaml
import re, requests
import random, hashlib
'''
Backlog:

* negative regex match support
* base class of FactDset: __DONE__
* start with, end with, contain, doesnot, equal function __DONE__
* example json with text not code: __DONE__
* using class to define each TestType Structures

* testcode: __DONE__
* validate function
'''

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import http.client  # or http.client if you're on Python 3
http.client._MAXHEADERS = 1000



AKAMAI_PRAGMA='akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-check-cacheable,akamai-x-get-cache-key,akamai-x-get-extracted-values,akamai-x-get-request-id,akamai-x-serial-no, akamai-x-get-true-cache-key'

def fractsingleton(cls):
    instances={}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance



class FractDset(object):
    HASSERT='hassert'
    HDIFF='hdiff'
    def __init__(self):
        self.query=dict()

    def init_template(self):
        pass

    def import_query(self, query_json):
        self.valid_query(query_json)
        self.query = json.loads(query_json)

    def valid_query(self, query):
        pass

    def export_query(self):
        return json.dumps(self.query)

    def __str__(self):
        return json.dumps(self.query)

    def set_comment(self, comment):
        '''
        update comment field
        '''
        assert type(comment) == type(str())
        self.query['Comment'] = comment

    def set_testid(self, testid=None):
        '''
        in: testid - testid text - if not set, hash val is set as a test id
        '''
        if testid is not None:
            self.query['TestId'] = str(testid)
        else:
            m=hashlib.sha256()
            m.update( str(random.random()).encode('utf-8'))
            m.update( json.dumps(self.query).encode('utf-8'))
            self.query['TestId'] = m.hexdigest()


class FractDsetFactory(object):
    '''
    Factory class to import FractDset family from json format
    '''
    @staticmethod
    def create(dsetjson):
        query=dict()
        if type(dsetjson) == type(str()):
            query = json.loads(dsetjson)
        elif type(dsetjson) == type(dict()):
            query=dsetjson
        else:
            raise Exception('FractDset arg type error')

        if query['TestType'] == FractDset.HASSERT:
            if 'Request' in query:
                obj=FractTestHassert()
                obj.query=query
                return obj
            elif 'ResultCase' in query:
                obj=FractResult()
                obj.query=query
                return obj
        elif query['TestType'] == FractDset.HDIFF:
            if 'RequestA' in query:
                obj=FractTestHdiff()
                obj.query=query
                return obj
            elif 'ResultCase' in query:
                obj=FractResult()
                obj.query=query
                return obj
        raise Exception('FractDset Type Error')
        return None




class FractSuiteManager(object):
    def __init__(self):
        self._suite=list()
    
    def load_base_suite(self, filename):
        with open(filename) as f:
            self._suite = json.load(f)
 
    def merge_suite(self, filename):
        '''
        returns # of merged and # of newly added
        '''
        cnt_merged=0
        cnt_added=0
        suite=list()
        with open(filename) as f:
            suite = json.load(f)
        for t in suite:
            testid = t['TestId']
            for base_t in self._suite:
                if base_t['TestId'] == testid:
                    base_t = t
                    cnt_merged+=1
                    break
            else:
                self._suite.append(t)
                cnt_added+=1

        assert cnt_merged + cnt_added == len(suite)
        return cnt_merged, cnt_added

    def get_suite(self):
        suite = list()
        for s in self._suite:
            frdset = FractDsetFactory.create(s) 
            suite.append(frdset)
        return suite

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self._suite, f)
        logging.debug('saved to {}\n'.format(filename))




class FractTest(FractDset):
    def __init__(self):
        super().__init__()
    
    def init_template(self):
        pass

    def init_example(self):
        pass
     

    def valid_query(self, query):
        pass

    def _str_summary(self):
        pass

class FractTestHassert(FractTest):
    def __init__(self):
        super().__init__()

    def init_template(self):
        self.query = { \
                'TestType': self.HASSERT,\
                'Request': {'Ghost': str(), 'Method':str(), 'Url':str(), 'Headers':dict() }, \
                'TestCase': dict(),\
                'Comment' : str(),\
                'TestId' : str()
                }

    def init_example(self):
        query_json='''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}]}}'''
        self.query = json.loads( query_json )
    
    def valid_query(self, query):
        pass

    def add(self, header, value, valtype='regex'):
        if header not in self.query['TestCase']:
            self.query['TestCase'][header] = list()
        self.query['TestCase'][header].append({'type':valtype, 'query':value})
    
    def setRequest(self, url, ghost, headers={}, method='GET'):
        self.query['Request']['Url']=url
        self.query['Request']['Ghost']=ghost
        self.query['Request']['Method']=method
        self.query['Request']['Headers']=headers

    def _str_summary(self):
        line=dict()
        line['Request'] = self.query['Request']
        return yaml.dump(line, default_flow_style=False)
        
    

class FractTestHdiff(FractTest):
    def __init__(self):
        super().__init__()

    def init_template(self):
        self.query = { \
                'TestType': self.HDIFF,\
                'RequestA': {'Ghost': str(), 'Method':str(), 'Url':str(), 'Headers':dict() }, \
                'RequestB': {'Ghost': str(), 'Method':str(), 'Url':str(), 'Headers':dict() }, \
                'TestCase': dict(),\
                'TestId'  : str(),\
                'Comment' : str()
                }

    def init_example(self):
        query_json='''{"TestType":"hdiff","Comment":"This is comment","TestID":"3606bd5770167eaca08586a8c77d05e6ed076899","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeaders":["Last-Modified","Cache-Control"]}'''
        self.query = json.loads( query_json )
    
    def valid_query(self, query):
        pass


    def _str_summary(self):
        line=dict()
        line['RequestA'] = self.query['RequestA']
        line['RequestB'] = self.query['RequestB']
        return yaml.dump(line, default_flow_style=False)
        




class FractResult(FractDset):
    def __init__(self):
        self.query={'TestType':str(),\
                'Passed' : bool(),\
                'Response': dict(),\
                'Comment' : str(), \
                'TestId' : str(), \
                'ResultCase': dict()}

    def init_template(self, TestType):
        pass

    def init_example(self, TestType):
        if TestType == FractResult.HASSERT:
            self.query = self._example_hassert()
        elif TestType == FractResult.HDIFF:
            self.query = self._example_hdiff()
        else:
            pass
    
    def _example_hassert(self):
        query_json='''{"TestType":"hassert","Comment":"This is Comment","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":false,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":false,"Value":301,"testcase":{"type":"regex","query":"(200|404)"}},{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":false,"Value":"This Header is not in Response","testcase":{"type":"regex","query":"text/html$"}}]}}'''
        return json.loads( query_json )

    def _example_hdiff(self):
        query_json = '''{"TestType":"hdiff","Passed":false,"Comment":"This is comment","TestId":"d704230e1206c259ddbb900004c185e46c42a32a","ResponseA":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResponseB":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":{"Passed":true,"Value":[301,301]},"Content-Length":{"Passed":false,"Value":[123,345]}}}'''
        return json.loads( query_json )

    def setTestType(self, TestType):
        assert TestType == FractResult.HASSERT or TestType == FractResult.HDIFF
        self.query['TestType'] = TestType

    def setPassed(self, passed):
        assert type(passed) == type(bool())
        self.query['Passed'] = passed

    def setResponse(self, status_code, response_headers, keyname='Response'):
        res = dict()
        res['status_code'] = status_code
        for k,v in response_headers.items():
            res[k] = v
        self.query[keyname] = res
        logging.debug('response: {}'.format(self.query['Response']))

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
        return (passed, cnt_test, cnt_passed, cnt_failed)

    def _str_resultcase(self, failed_only=False):
        '''
        ex)
        status_code
          * Passed: False
          * Assertion: regex: "(200|404)"
          * Response: 301
        
        Resonse Header: Content-Type
          * Passed: False
          * Assertion: regex

        '''
        assert self.query['TestType'] in (FractResult.HASSERT, FractResult.HDIFF)
        line=dict()
        if self.query['TestType'] == FractResult.HASSERT:
            for headername, retlist in self.query['ResultCase'].items():
                line[headername] = list()
                for ret in retlist:
                    if failed_only and ret['Passed']:
                        continue
                    case=dict()
                    case['Passed'] = ret['Passed']
                    case['TestAssert'] = '{}: "{}"'.format(ret['testcase']['type'], ret['testcase']['query'])
                    case['Response']= ret['Value']
                    line[headername].append(case)
                else:
                    if not line[headername] :
                        del line[headername]
        
        elif self.query['TestType'] == FractResult.HDIFF:
            for headername, ret in self.query['ResultCase'].items():
                line[headername] = dict()
                if failed_only and ret['Passed']:
                    del line[headername]
                    continue
                line[headername]['Passed'] = ret['Passed']
                line[headername]['ResponseA'] = ret['Value'][0]
                line[headername]['ResponseB'] = ret['Value'][1]

        return yaml.dump(line, default_flow_style=False)


@fractsingleton
class Actor(object):
    '''
    role as factory of requests.response object
    '''
    def __init__(self):
        self.session=requests.Session()

    def get(self, url, headers=None, ghost=None, ssl_verify=False):
        '''
        return ActorResponse object
        '''
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

        # throw the http request
        r = self.session.get(req_url, headers=req_headers, verify=ssl_verify, allow_redirects=False)
        logging.debug(req_url)
        logging.debug(req_headers)
        
        return ActorResponse(r)

class ActorResponse(object):
    '''
    This object will be created by class Actor
    '''
    def __init__(self, response):
        'in: response is requests.Response object'
        #self.r = requests.Response()
        self.r = response
    def headers(self):
        hdr = self.r.headers
        hdr['status_code'] = self.r.status_code
        return hdr
    def resh(self, headername):
        if headername == 'status_code':
            return self.r.status_code
        return self.r.headers[ headername ]
    def status_code(self):
        return self.r.status_code


class Fract(object):
    def __init__(self):
        self.actor=Actor()

    def run(self, fracttest):
        if fracttest.query['TestType'] == FractDset.HASSERT:
            return self._run_hassert(fracttest)
        elif fracttest.query['TestType'] == FractDset.HDIFF:
            return self._run_hdiff(fracttest)
        else:
            pass # should throw exception
        return None
        
    def _throw_request(self, fractreq):
        '''
        input: fract request dict" like {"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}}
        return: response object of 'requests' lib
        '''
        url = fractreq['Url']
        ghost = fractreq['Ghost']
        headers = fractreq['Headers']
        
        # throw HTTP request
        return self.actor.get( url, headers, ghost )


    def _run_hassert(self, fracttest):
        '''
        input: FractTest object
        return: FractResult object

        '''
        res = FractResult()
        res.setTestType(FractResult.HASSERT)
        res.set_testid(fracttest.query['TestId'])

        # throw HTTP request
        actres = self._throw_request(fracttest.query['Request'])
        res.setResponse(actres.status_code, actres.headers() )
        
        # validation process
        for hdr,tlist in fracttest.query['TestCase'].items(): ### Per Header
            res.query['ResultCase'][hdr] = self._check_headercase(hdr, tlist, actres.headers())
            
        # check if passed at whole testcase
        psd = res.check_passed()
        logging.debug('ResultCase: {}'.format(res))

        return res

    def _run_hdiff(self, fracttest):
        '''
        input: FractTest object
        return: FractResult object
        '''
        res = FractResult()
        res.setTestType(FractResult.HDIFF)
        res.set_testid(fracttest.query['TestId'])
        res.query['ResultCase'] = dict()

        # throw HTTP request
        actresA= self._throw_request(fracttest.query['RequestA'])
        actresB= self._throw_request(fracttest.query['RequestB'])
        
        res.setResponse(actresA.status_code, actresA.headers(), 'ResponseA' )
        res.setResponse(actresB.status_code, actresB.headers(), 'ResponseB' )

        # validation process
        for vh in fracttest.query['VerifyHeaders']:
            logging.debug('_run_diff(): verify header ==> {}'.format(vh))
            valA=str()
            valB=str()
            if vh in actresA.headers():
                valA=actresA.resh(vh)
            else:
                valA='N/A'
            if vh in actresB.headers():
                valB=actresB.resh(vh)
            else:
                valB='N/A'

            res.query['ResultCase'][vh] = {'Passed': valA==valB, 'Value': [valA, valB]}
        
        
        # check if passed at whole testcase
        # should be replaced later with chech_passed() functions
        passed=True
        for k,v in res.query['ResultCase'].items():
            if v['Passed'] == False:
                passed=False
                break
        res.query['Passed'] = passed
        
        logging.debug('ResultCcase: {}'.format(res))
        return res


    def _check_headercase(self, header_name, testlist, response_header):
        '''
        return: list of test result per header:
            ex) [{"Passed":false,"Value":301,"testcase":{"type":"regex","query":"(200|404)"}},{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}]
        '''
        hdr_resultcase = list()
        has_this_header = False
        if header_name in response_header:
            has_this_header = True
            logging.debug('hdr value: {}: {}'.format(header_name, response_header[ header_name ]))
        else:
            logging.debug('hdr value: {}: Not Included on Response'.format(header_name))

        # parse each testcase
        for t in testlist:
            logging.debug('  --> test={}'.format(t))
            assert t['type'] == 'regex'

            if has_this_header:
                hdr_resultcase.append(\
                        {'Passed': self._passed(t['type'], t['query'], str(response_header[ header_name ]) ),\
                        'Value': response_header[ header_name ],\
                        'testcase': t })
            else: # header not in response
                logging.debug('  -> test failed: testcase={}'.format(t['query']) )
                hdr_resultcase.append(\
                        {'Passed': False,\
                        'Value':'This Header is not in Response',\
                        'testcase': t })
            
        #res.query['ResultCase'][header_name] = hdr_resultcase            
        return hdr_resultcase
    
    def _passed(self, mode, query, text):
        'return (bool) passed'

        if mode == 'regex':
            match = re.search( query, text)
            if match is not None:
                return True
            else:
                return False
        elif mode == 'startswith':
            return text.startswith(query)
        elif mode == 'endswith':
            return text.endswith(query)
        elif mode == 'contain':
            if text.find(query) != -1:
                return True
            else:
                return False
        else:
            pass # should raise exception!


class FractClient(object):
    '''
    This class for run Fract test suite and other useful tasks
    '''
    def __init__(self, fract_suite_json=None, fract_suite_file=None, fract_suite_obj=None):
        self._testsuite = list()
        self._testsuiteId = dict() # dict data to search by TestId
        _test_list = None
        
        
        if fract_suite_obj is not None:
            self._testsuite = fract_suite_obj
            for t in self._testsuite:
                self._testsuiteId[ t.query['TestId'] ] = t
                logging.warning(t.query['TestId'])

        else:
            if fract_suite_json is not None:
                _test_list = json.loads(fract_suite_json)
            elif fract_suite_file is not None:
                with open(fract_suite_file) as f:
                    _test_list = json.load(f)

            if _test_list is not None:
                for t in _test_list:
                    #f=FractTest()
                    #f.import_query( json.dumps(t) )
                    f = FractDsetFactory.create( json.dumps(t) )
                    self._testsuite.append(f)
                    self._testsuiteId[f.query['TestId']] = f
            else:
                self._testsuite = list()
        
        self.fract = Fract()
        self._result_suite = list()
        self._failed_result_suite=list()

    def _get_testcase(self, TestId):
        return self._testsuiteId[ TestId ] 

    def load_resultfile(self, resultfile):
        '''
        load date from files and set it to following data
        * self._result_suite
        * self._failed_result_suite
        '''
        with open(resultfile) as f:
            retlist = json.load(f)
            for ret in retlist:
                fret = FractDsetFactory.create( json.dumps(ret) )
                self._result_suite.append( fret )
                if not fret.query['Passed']:
                    self._failed_result_suite.append( fret )
                    

    def load_result(self, s_result):
        self._result_suite = s_result
        for fret in self._result_suite:
            if not fret.query['Passed']:
                self._failed_result_suite.append( fret )




    def run_suite(self, testids=None):
        for t in self._testsuite:
            if testids is not None and t.query['TestId'] in testids:
                ret=self.fract.run(t)
                self._result_suite.append( ret )
                logging.debug(ret)
                if not ret.query['Passed']:
                    self._failed_result_suite.append( ret )
            elif testids is None:
                ret=self.fract.run(t)
                self._result_suite.append( ret )
                if not ret.query['Passed']:
                    self._failed_result_suite.append( ret )
            else:
                pass
        logging.debug('# of failed: {}'.format(len(self._failed_result_suite)))
    
    def export_result(self, filename='fract_default.txt'):
        ret_dict = list()
        for ret in self._result_suite:
            ret_dict.append( ret.query )

        with open(filename, 'w') as f:
            f.write(json.dumps(ret_dict, indent=2))

    def export_failed_testsuite(self, filename, fmt='json'):
        assert fmt in ('json', 'yaml')
        failed_tests=list()
        for failed_ret in self._failed_result_suite:
            t = self._get_testcase( failed_ret.query['TestId'] )
            failed_tests.append( t.query )
        
        with open(filename, 'w') as f:
            if fmt == 'json':
                f.write(json.dumps( failed_tests, indent=2))
            elif fmt == 'yaml':
                f.write(yaml.dump( failed_tests, default_flow_style=False))


    def make_summary(self):
        '''
        self.summary=dict():
        {
        'total':30, 
        'failed':[ {'testid': abc123456, [ --failed-result-case--, ... ]}, ...]
        }

        Summary is like this: markdown format

        Summary
        =====================

        test not passed
        ---------------------

        ### testid: 3606bd5770167eaca08586a8c77d05e6ed076899
        
        X-Cache-Key:
        - Passed: false
          Value: S/D/13100/570031/000/space.ktmrmshk.com/space/?akamai-transform=9 cid=___EDC_IS_MOBILE=false
          testcase: {query: /570032/, type: regex}
        

        ### testid: d449493f0df74c73a77ae99ec738d1007e57b8b395975da023de2b321890423f
         ....
         ....


        total
        --------------------
        ran 30 tests: 4 failed
        '''
        summary=str()
        summary+='''
Summary
=================

Tests not passed
----------------\n'''

        cnt_testcase=len( self._result_suite )
        cnt_failed=len( self._failed_result_suite )
        for ret in self._failed_result_suite:
            summary+='### TestId: {}\n\n'.format(ret.query['TestId'])
            t = self._get_testcase( ret.query['TestId'] )
            print(type(t))
            summary += t._str_summary()
            summary+='\n'
            
            summary+=ret._str_resultcase(True)
            summary+='\n\n'
        summary+='''
Total
----------------\n'''
        summary+='ran {} tests: {} failed\n\n'.format(cnt_testcase, cnt_failed)
        if cnt_failed == 0:
            summary+='=> OK\n'
        else:
            summary+='=> Not Good\n'

        #print(summary)
        return summary

    def print_result(self):
        cnt_test=0
        cnt_error=0
        for ret in self._result_suite:
            if ret.query['Passed'] == False:
                cnt_error+=1
            else:
                assert ret.query['Passed'] == True
            cnt_test+=1

        print('--------------------------')
        print('Ran {} tests / {} errors'.format(cnt_test, cnt_error))
        if cnt_error == 0:
            print('=> OK')
        else:
            print('=> Not Good')



class JsonYaml(object):
    def __init__(self):
        pass
    def j2y(self, jsonfile, yamlfile):
        with open(jsonfile) as fr:
            obj = json.load(fr)
            with open(yamlfile, 'w') as fw:
                fw.write(yaml.dump(obj, default_flow_style=False))

    def y2j(self, yamlfile, jsonfile):
        with open(yamlfile) as fr:
            lines=fr.read()
            obj=yaml.load(lines)
            with open(jsonfile, 'w') as fw:
                json.dump(obj, fw)




import sys
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    def usage():
        print('usage: $ pyton3 fract.py input.json output.json')

    if len(sys.argv) != 3:
        usage()
        exit()

    testsuite_json=str()
    with open(sys.argv[1]) as f:
        testsuite_json = f.read()    
    fclient = FractClient(testsuite_json)
    fclient.run_suite()
    fclient.export_result(sys.argv[2])
    fclient.print_result()





