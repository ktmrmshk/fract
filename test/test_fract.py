import unittest, json, logging, re

from fract import FractTest, FractTestHassert, FractTestHdiff
class test_FractTest(unittest.TestCase):
    def setUp(self):
        self.fracttest = FractTest()
    def tearDown(self):
        pass
    
    def test_init_template1(self):
        ft=FractTestHassert()
        ft.init_template()
        self.assertTrue( 'TestType' in ft.query )
        self.assertTrue( ft.query['TestType'] == 'hassert')
        self.assertTrue( 'Comment' in ft.query )
        self.assertTrue( 'TestId' in ft.query )

    def test_init_template2(self):
        ft=FractTestHdiff()
        ft.init_template()
        self.assertTrue( 'TestType' in ft.query )
        self.assertTrue( ft.query['TestType'] == 'hdiff')
        self.assertTrue( 'RequestA' in ft.query )
        self.assertTrue( 'RequestB' in ft.query )
        self.assertTrue( 'TestCase' in ft.query )
        self.assertTrue( 'TestId' in ft.query )
        self.assertTrue( 'Comment' in ft.query )
               
    def test_init_example_1(self):
        ft=FractTestHassert()
        
        ft.init_example()
        self.assertTrue( ft.query['TestType'] == 'hassert' )
    
    def test_init_example_2(self):
        ft=FractTestHdiff()

        ft.init_example()
        self.assertTrue( ft.query['TestType'] == 'hdiff' )

    def test_import_query(self):
        self.fracttest.import_query('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}],"Location":[{"type":"regex","query":"https://www.akamai.com"}]}} ''')
        self.assertTrue( self.fracttest.query['TestType'] == 'hassert' )

    def test_add1(self):
        ft = FractTestHassert()
        ft.init_template()
        ft.add('status_code', '(301|302)')
        ft.add('status_code', '301')
        logging.warning(json.dumps(ft.query))
        self.assertTrue( ft.query['TestCase'] == {"status_code": [{"type": "regex", "query":"(301|302)" }, {"type": "regex", "query":"301"}]})
    
    # 2018/08/21 ignore_case support
    def test_add2_option(self):
        ft = FractTestHassert()
        ft.init_template()
        ft.add('X-Cache-Key', '/FooBar/', 'contain', {'ignore_case': True})
        logging.warning(json.dumps(ft.query))
        self.assertTrue( ft.query['TestCase'] == {"X-Cache-Key": [{"type": "contain", "query":"/FooBar/", "option" :{"ignore_case": True} }]})
    
    def test_setRequest1(self):
        ft = FractTestHassert()
        ft.init_template()
        ft.setRequest('http://www.akamai.com/', 'www.akamai.com.edgekey.net')
        self.assertTrue( ft.query['Request']['Url'] == 'http://www.akamai.com/')
        self.assertTrue( ft.query['Request']['Ghost'] == 'www.akamai.com.edgekey.net')
        self.assertTrue( ft.query['Request']['Method'] == 'GET')
        
    def test_set_comment(self):
        ft = FractTestHassert()
        ft.init_template()
        ft.set_comment('abc=123')
        self.assertTrue( ft.query['Comment'] == 'abc=123')

    def test_set_testid(self):
        ft = FractTestHassert()
        ft.init_template()
        ft.set_testid('hogehoge')
        self.assertTrue( ft.query['TestId'] == 'hogehoge')

        ft.set_testid()
        self.assertTrue( ft.query['TestId'] != 'hogehoge')

    def test_set_loadtime(self):
        ft = FractTestHassert()
        ft.init_template()
        ft.set_loadtime(0.123)
        self.assertTrue( ft.query['LoadTime'] == 0.123)

    def test_str_summary_hassert(self):
        ft = FractTestHassert()
        ft.init_example()
        self.assertTrue( type(ft._str_summary() ) == type(str()) )
        print( ft._str_summary() )

    def test_str_summary_hdiff(self):
        ft = FractTestHdiff()
        ft.init_example()
        self.assertTrue( type(ft._str_summary() ) == type(str()) )
        print( ft._str_summary() )


from fract import FractDsetFactory
class test_FractDsetFactory(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_init1(self):
        ft = FractTestHassert()
        ft.init_example()
        jsontxt = ft.__str__()
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractTestHassert() ))

    def test_init2(self):
        ft = FractTestHdiff()
        ft.init_example()
        jsontxt = ft.__str__()
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractTestHdiff() ))

    def test_init3(self):
        ft = FractResult()
        ft.init_example(FractResult.HASSERT)
        jsontxt = ft.__str__()
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractResult() ))

    def test_init4(self):
        ft = FractResult()
        ft.init_example(FractResult.HDIFF)
        jsontxt = ft.__str__()
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractResult() ))

    def test_init11(self):
        ft = FractTestHassert()
        ft.init_example()
        jsontxt = ft.query
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractTestHassert() ))

    def test_init12(self):
        ft = FractTestHdiff()
        ft.init_example()
        jsontxt = ft.query
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractTestHdiff() ))

    def test_init13(self):
        ft = FractResult()
        ft.init_example(FractResult.HASSERT)
        jsontxt = ft.query
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractResult() ))

    def test_init14(self):
        ft = FractResult()
        ft.init_example(FractResult.HDIFF)
        jsontxt = ft.query
        obj = FractDsetFactory.create(jsontxt)
        self.assertTrue( type(obj) == type(FractResult() ))





from fract import FractSuiteManager
class test_FractSuiteManager(unittest.TestCase):
    def test_load_base_suite(self):
        ftm = FractSuiteManager()
        ftm.load_base_suite('testcase4test.json')
        self.assertTrue( len(ftm._suite) == 32)
        #logging.warning( ftm._testsuite )

    def test_merge_suite(self):
        ftm = FractSuiteManager()
        ftm.load_base_suite('testcase4test.json')
        ret = ftm.merge_suite('testcase4test_sub.json')
        self.assertTrue( ret == (1,1) )
        self.assertTrue( len(ftm._suite) == 33)

    def test_merge_suite2(self):
        ftm = FractSuiteManager()
        ftm.load_base_suite('resutlcase4test.json')
        ret = ftm.merge_suite('resultcase4test_sub.json')
        self.assertTrue( ret == (1,1) )
        self.assertTrue( len(ftm._suite) == 33)
        ftm.save('final_result.json')


    def test_save(self):
        ftm = FractSuiteManager()
        ftm.load_base_suite('testcase4test.json')
        ftm.save('foobar.json')

    def test_get_suite(self):
        ftm = FractSuiteManager()
        ftm.load_base_suite('testcase4test.json')
        a=ftm.get_suite()
        logging.warning('type of a is {}'.format(type(a[0])))
        self.assertTrue( type(a[0]) == type(FractTestHassert() ) )
        
    def test_get_suite2(self):
        ftm = FractSuiteManager()
        ftm.load_base_suite('resutlcase4test.json')
        a=ftm.get_suite()
        logging.warning('type of a is {}'.format(type(a[0])))
        self.assertTrue( type(a[0]) == type(FractResult() ) )
        

from fract import FractResult
class test_FracResult(unittest.TestCase):
    def setUp(self):
        self.fractresult = FractResult()
    def tearDown(self):
        pass

    def test_init_example1(self):
        self.fractresult.init_example('hassert')
        self.assertTrue( self.fractresult.query['TestType'] == 'hassert' )

    def test_init_example2(self):
        self.fractresult.init_example('hdiff')
        self.assertTrue( self.fractresult.query['TestType'] == 'hdiff' )

    def test_setTestType(self):
        self.fractresult.setTestType('hassert')
        self.assertTrue( self.fractresult.query['TestType'] == 'hassert' )

    def test_setPassed(self):
        self.fractresult.setPassed(False)
        self.assertTrue( self.fractresult.query['Passed'] == False )

    def test_setResponse(self):
        self.fractresult.setResponse( 403, {'Content-Length': 123, 'Vary': 'User-Agent'})
        self.assertTrue( self.fractresult.query['Response']['status_code'] == 403 )
        self.assertTrue( self.fractresult.query['Response']['Vary'] == 'User-Agent' )

    def test_check_passed1(self):
        self.fractresult.query=json.loads( '''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":false,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":false,"Value":301,"TestCase":{"type":"regex","query":"(200|404)"}},{"Passed":true,"Value":301,"TestCase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":false,"Value":"This Header is not in Response","TestCase":{"type":"regex","query":"text/html$"}}]}} ''' )
        ret = self.fractresult.check_passed()
        self.assertTrue( ret == (False, 3, 1, 2) )

    def test_check_passed2(self):
        self.fractresult.query=json.loads('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":true,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":true,"Value":301,"TestCase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":true,"Value":"text/html","TestCase":{"type":"regex","query":"text/html$"}}]}}''')
        ret = self.fractresult.check_passed()
        self.assertTrue( ret == (True, 2, 2, 0) )

    def test_str_resultcase(self):
        self.fractresult.query=json.loads('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":true,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":true,"Value":301,"TestCase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":true,"Value":"text/html","TestCase":{"type":"regex","query":"text/html$"}}]}}''')
        ret=self.fractresult._str_resultcase( True )
        self.assertTrue( type(ret) == type(str()))
        logging.warning( ret )

    # 2018/08/21 ignore_case support
    def test_str_resultcase_option(self):
        self.fractresult.query=json.loads('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":true,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":true,"Value":301,"TestCase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":true,"Value":"text/html","TestCase":{"type":"regex","query":"text/html$"}}]}}''')
        ret=self.fractresult._str_resultcase(  )
        self.assertTrue( type(ret) == type(str()))
        logging.warning( ret )

    def test_str_resultcase_option2(self):
        self.fractresult.query=json.loads('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":true,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":true,"Value":301,"TestCase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":true,"Value":"text/html","TestCase":{"type":"regex","query":"text/html$","option":{"ignore_case":true,"not":false}}}]}}''')
        ret=self.fractresult._str_resultcase(  )
        self.assertTrue( type(ret) == type(str()))
        logging.warning( ret )

    def test_str_resultcase2(self):
        self.fractresult.query=json.loads('''{"TestType":"hdiff","Passed":false,"Comment":"This is comment","TestId":"d704230e1206c259ddbb900004c185e46c42a32a","ResponseA":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResponseB":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":{"Passed":true,"Value":[301,301]},"Content-Length":{"Passed":false,"Value":[123,345]}}}''')
        ret=self.fractresult._str_resultcase( True )
        self.assertTrue( type(ret) == type(str()))
        logging.warning( ret )


from fract import Actor, ActorResponse
class test_Actor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor()
        #self.actorresponse = self.actor.get('https://space.ktmrmshk.com/abc/example.html?abc=123', ghost='space.ktmrmshk.com.edgekey-staging.net', headers={'Accept-Encoding': 'gzip'})
        # 2019/10/21 For Botman Start
        self.actorresponse = self.actor.get('https://space.ktmrmshk.com/abc/example.html?abc=123', ghost='space.ktmrmshk.com.edgekey-staging.net', headers={'Accept-Encoding': 'gzip', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'})
        # 2019/10/21 For Botman End
    def tearDown(self):
        pass

    def test_get(self):
        self.assertTrue( self.actorresponse.r.status_code != 400 )

    def test_get_headers(self):
        self.assertTrue( 'status_code' in self.actorresponse.headers() )

    def test_get_status_code(self):
        self.assertTrue( self.actorresponse.status_code() == self.actorresponse.r.status_code ) 

    def test_resh(self):
        self.assertTrue( self.actorresponse.resh('status_code') == self.actorresponse.r.status_code )
        self.assertTrue( self.actorresponse.resh('Date') == self.actorresponse.r.headers['Date'] )
    
    #2018/12/04 Rum-off Start
    def test_resh_null_response_header(self):
        self.assertTrue( self.actorresponse.resh('NothingNothingNothing') == '' )
    #2018/12/04 Rum-off End

    def test_siggleton(self):
        a = Actor()
        b = Actor()
        self.assertTrue( a == b)


    def test_getLoadTime(self):
        self.assertTrue( type(self.actorresponse.getLoadTime()) == type(1.23))

from fract import Fract
class test_Fract(unittest.TestCase):
    def setUp(self):
        self.fr = Fract()
    def tearDown(self):
        pass

    def test_run_hassert(self):
        testcase = FractTestHassert()
        testcase.import_query('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}],"Location":[{"type":"regex","query":"https://www.akamai.com"}]}} ''')
        ret = self.fr._run_hassert(testcase)
        self.assertTrue( ret.query['TestType'] == 'hassert')
        self.assertTrue( ret.query['Passed'] == False )
        logging.info('FractResult: {}'.format(ret))

    def test_passed(self):
        self.assertTrue( self.fr._passed('regex', '(200|404)', '404') )
        self.assertFalse( self.fr._passed('regex', '(200|404)', '403') )
        self.assertTrue( self.fr._passed('startswith', 'http://', 'http://www.jins.com') )
        self.assertFalse( self.fr._passed('startswith', 'http://', 'https://www.jins.com') )
        self.assertTrue( self.fr._passed('endswith', '.com', 'http://www.jins.com') )
        self.assertFalse( self.fr._passed('endswith', '.com', 'https://www.jins.co.jp') )
        self.assertTrue( self.fr._passed('contain', 'jins', 'http://www.jins.com') )
        self.assertFalse( self.fr._passed('contain', 'jeans', 'https://www.jins.co.jp') )
        
        self.assertTrue( self.fr._passed('regex', re.escape('http://abc.com/index.html?xyz=123&Name=FOOBAR'), 'http://abc.com/index.html?xyz=123&Name=FOOBAR') )
        self.assertTrue( self.fr._passed('exact', 'http://abc.com/index.html?xyz=123&Name=FOOBAR', 'http://abc.com/index.html?xyz=123&Name=FOOBAR') )
        self.assertFalse( self.fr._passed('exact', 'https://abc.com/index.html?xyz=123&Name=FOOBAR', 'http://abc.com/index.html?xyz=123&Name=FOOBAR') )

    # 2018/08/21 ignore_case support
    def test_passed_ignore_case(self):
        self.assertTrue( self.fr._passed('regex', '(200|404)', '404', True) )
        self.assertTrue( self.fr._passed('regex', '(200|404)', '404', False) )
        self.assertFalse( self.fr._passed('regex', '(200|404)', '403', False) )
        self.assertTrue( self.fr._passed('startswith', 'http://', 'hTTp://www.jins.com', True) )
        self.assertFalse( self.fr._passed('startswith', 'http://', 'https://www.jins.com', True) )
        self.assertTrue( self.fr._passed('endswith', '.com', 'http://www.jins.COM', True) )
        self.assertFalse( self.fr._passed('endswith', '.com', 'https://www.jins.co.jp', True) )
        self.assertTrue( self.fr._passed('contain', 'jins', 'http://www.JIns.com', True) )
        self.assertFalse( self.fr._passed('contain', 'jins', 'http://www.JIns.com') )
        self.assertFalse( self.fr._passed('contain', 'jins', 'http://www.JIns.com', False) )
        self.assertFalse( self.fr._passed('contain', 'jeans', 'https://www.jins.co.jp') )
        
        self.assertTrue( self.fr._passed('regex', re.escape('http://abc.com/index.html?xyz=123&Name=FOOBAR'), 'http://abc.com/index.html?xyz=123&Name=foobar', True) )
        self.assertTrue( self.fr._passed('exact', 'http://abc.com/index.html?xyz=123&Name=FOOBAR', 'http://abc.com/index.html?xyz=123&Name=foobar', True) )
        self.assertFalse( self.fr._passed('exact', 'https://abc.com/index.html?xyz=123&Name=FOOBAR', 'http://abc.com/index.html?xyz=123&Name=FOOBAR') )


    def test_check_headercase(self):
        ret = self.fr._check_headercase('status_code', [{"type":"regex","query":"301"}], {'status_code': 301})
        self.assertTrue( ret[0]['Passed'] == True )
        self.assertTrue( ret[0]['Value'] == 301 )
        self.assertTrue( ret[0]['TestCase']['type'] == 'regex' )


    # 2018/08/21 ignore_case support
    def test_check_headercase2(self):
        ret = self.fr._check_headercase('X-Cache-Key', [{"type":"regex","query":"/HOGE/foo/bar"}], {'X-Cache-Key': 'D/S/123/hoge/foo/bar/dot.jpg'})
        self.assertTrue( ret[0]['Passed'] == False )
        self.assertTrue( ret[0]['Value'] == 'D/S/123/hoge/foo/bar/dot.jpg' )
        self.assertTrue( ret[0]['TestCase']['type'] == 'regex' )

    def test_check_headercase3(self):
        ret = self.fr._check_headercase('X-Cache-Key', [{"type":"regex","query":"/HOGE/foo/bar","option":{"ignore_case":True}}], {'X-Cache-Key': 'D/S/123/hoge/foo/bar/dot.jpg'})
        self.assertTrue( ret[0]['Passed'] == True )

    def test_check_header_gclid(self):
        testcase = FractTestHdiff()
        testcase.import_query('''{"TestType": "hassert", "Request": {"Ghost": "a850.dscr.akamai-staging.net", "Method": "GET", "Url": "https://fract.akamaized-staging.net/testing/gclid/first", "Headers": {"User-Agent": "MacOS", "Pragma": "akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-check-cacheable,akamai-x-get-cache-key,akamai-x-get-extracted-values,akamai-x-get-request-id,akamai-x-serial-no, akamai-x-get-true-cache-key", "X-Akamai-Cloudlet-Cost": "true", "Cookie": "akamai-rum=off"}}, "TestCase": {"X-Cache-Key": [{"type": "regex", "query": "/728260/", "option": {"ignore_case": false}}, {"type": "regex", "query": "/000/", "option": {"ignore_case": false}}, {"type": "contain", "query": "/fract.akamaized-staging.net/col", "option": {"ignore_case": false}}], "status_code": [{"type": "regex", "query": "302", "option": {"ignore_case": false}}], "Location": [{"type": "exact", "query": "https://fract.akamaized-staging.net/testing/gclid/first?gclid=EAIaIQobChMIodSq1veA4wIVQXZgCh2QGQmGEAAYASAAEgKs3_D_BwE&_ga=2.108142722.1227508989.1571126780-1104359897.1571126780&utm_medium=email&utm_source=uq_html&utm_term=uh_191016_crm_welcome5&abc=123&123=abc", "option": {"ignore_case": false}}]}, "Comment": "This test was gened by FraseGen - v1.04 at 2019/10/21, 17:26:22 JST", "TestId": "88fe95419ddb43f5dd95cd6cde44c50687a54c73127284d06b70d59fd90540fd", "Active": true, "LoadTime": 0.180052} ''')
        ret = self.fr.run(testcase)
        self.assertTrue( ret.query['TestType'] == 'hassert')
        self.assertTrue( ret.query['Passed'] == True )
        self.assertTrue( 'LoadTime' in ret.query )
        logging.info('FractResult: {}'.format(ret))


    def test_run_hdiff(self):
        testcase = FractTestHdiff()
        testcase.import_query('''{"TestType":"hdiff","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeaders":["Last-Modified","Cache-Control", "status_code", "Content-Length"]} ''')
        fr =Fract()
        ret = fr._run_hdiff(testcase)
        logging.warning('fractresult= {}'.format(ret))
        self.assertTrue( ret.query['TestType'] == 'hdiff')

    def test_run1(self):
        testcase = FractTest()
        testcase.import_query('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}],"Location":[{"type":"regex","query":"https://www.akamai.com"}]}} ''')
        ret = self.fr.run(testcase)
        self.assertTrue( ret.query['TestType'] == 'hassert')
        self.assertTrue( ret.query['Passed'] == False )
        self.assertTrue( 'LoadTime' in ret.query )
        logging.info('FractResult: {}'.format(ret))
        
    def test_run2(self):
        testcase = FractTest()
        testcase.import_query('''{"TestType":"hdiff","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeaders":["Last-Modified","Cache-Control", "status_code", "Content-Length"]} ''')
        fr =Fract()
        ret = fr.run(testcase)
        logging.warning('fractresult= {}'.format(ret))
        self.assertTrue( ret.query['TestType'] == 'hdiff')

    # 2018/08/21 ignore_case support
    def test_run_ignore_case_failed(self):
        testcase = FractTest()
        testcase.import_query('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"TEXT/html$"}],"Location":[{"type":"regex","query":"https://WWW.akamai.COM","option":{"ignore_case":false}}]}}''')
        ret = self.fr.run(testcase)
        self.assertTrue( ret.query['TestType'] == 'hassert')
        self.assertTrue( ret.query['Passed'] == False )
        self.assertTrue( ret.query['ResultCase']['Content-Type'][0]['Passed'] == False )
        self.assertTrue( ret.query['ResultCase']['Location'][0]['Passed'] == False )
        self.assertTrue( ret.query['ResultCase']['Location'][0]['TestCase']['option']['ignore_case'] == False )
        logging.warning('FractResult: {}'.format(ret))
 
    def test_run_ignore_case_passed(self):
        testcase = FractTest()
        testcase.import_query('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404|302|301)"}],"Connection":[{"type":"regex","query":"KeeP","option":{"ignore_case":true}}],"Location":[{"type":"contain","query":"https://WWW.akamai.COM","option":{"ignore_case":true}}]}}''')
        ret = self.fr.run(testcase)
        logging.warning('FractResult: {}'.format(ret))
        self.assertTrue( ret.query['TestType'] == 'hassert')
        self.assertTrue( ret.query['Passed'] == True )
        self.assertTrue( ret.query['ResultCase']['Connection'][0]['Passed'] == True )
        self.assertTrue( ret.query['ResultCase']['Location'][0]['Passed'] == True )
        self.assertTrue( ret.query['ResultCase']['Location'][0]['TestCase']['option']['ignore_case'] == True )
 
    def test_run2(self):
        testcase = FractTest()
        testcase.import_query('''{"TestType":"hdiff","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeaders":["Last-Modified","Cache-Control", "status_code", "Content-Length"]} ''')
        fr =Fract()
        ret = fr.run(testcase)
        logging.warning('fractresult= {}'.format(ret))
        self.assertTrue( ret.query['TestType'] == 'hdiff')

    # 2018/08/21 ignore_case support
    
    def test_run_active_filed(self):
        testcase = FractTest()
        testcase.import_query('''{"Active":true,"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}],"Location":[{"type":"regex","query":"https://www.akamai.com"}]}} ''')
        ret = self.fr.run(testcase)
        self.assertTrue( ret.query['TestType'] == 'hassert')
        self.assertTrue( ret.query['Passed'] == False )
        logging.info('FractResult: {}'.format(ret))


    def test_run_inactive(self):
        testcase = FractTest()
        testcase.import_query('''{"Active":false,"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}],"Location":[{"type":"regex","query":"https://www.akamai.com"}]}} ''')
        ret = self.fr.run(testcase)
        self.assertTrue( ret is None)


from fract import FractClient
class test_FractClient(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.testsuite = '''[{"TestType":"hassert","Comment":"This is comment","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}]}},{"TestType":"hdiff","Comment":"This is comment","TestId":"d704230e1206c259ddbb900004c185e46c42a32a","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeaders":["Last-Modified","Cache-Control"]}]'''

    def test_init(self):
        fclient = FractClient(self.testsuite)
        self.assertTrue( len(fclient._testsuite) ==2 )

    def test_init2(self):
        fclient = FractClient(fract_suite_file='testcase4test.json')
        self.assertTrue( len(fclient._testsuite) == 32 )
    
    def test_run_suite(self):
        fclient = FractClient(self.testsuite)
        fclient.run_suite()
        self.assertTrue( len(fclient._result_suite) ==2 )
        logging.info('test_run_suite(): _result_suite={}'.format(fclient._result_suite[0]))
        
        fclient.export_result()
    
    def test_run_suite2(self):
        fclient = FractClient(self.testsuite)
        fclient.run_suite( ['d704230e1206c259ddbb900004c185e46c42a32a'])
        self.assertTrue( len(fclient._result_suite) ==1 )
        self.assertTrue( len(fclient._failed_result_suite) == 0)
        logging.info('test_run_suite(): _result_suite={}'.format(fclient._result_suite[0]))
        
        fclient.export_result()
 
    def test_run_suite_inactive_test(self):
        testjson='''[{"Active":true,"TestType":"hassert","Comment":"This is comment","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}]}},{"TestType":"hdiff","Comment":"This is comment","TestId":"d704230e1206c259ddbb900004c185e46c42a32a","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeaders":["Last-Modified","Cache-Control"]},{"Active":false,"TestType":"hassert","Comment":"This is comment","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}]}}]'''
        fclient = FractClient(testjson)
        fclient.run_suite()
        self.assertTrue( len(fclient._result_suite) == 2 )
        logging.info('test_run_suite(): _result_suite={}'.format(fclient._result_suite[0]))
        fclient.export_result()


    def test_make_summary(self):
        fclient = FractClient(self.testsuite)
        fclient.run_suite()
        fclient.make_summary()

    def test_get_testcase(self):
        fclient = FractClient(self.testsuite)
        t = fclient._get_testcase('d704230e1206c259ddbb900004c185e46c42a32a')
        self.assertTrue(t.query['TestId'] == 'd704230e1206c259ddbb900004c185e46c42a32a')

    def test_export_failed_testsuite(self):
        fclient = FractClient(self.testsuite)
        fclient.run_suite( ['3606bd5770167eaca08586a8c77d05e6ed076899'])
        fclient.export_failed_testsuite('diff.json')

    def test_load_resultfile(self):
        fclient = FractClient(self.testsuite)
        fclient.load_resultfile('resutlcase4test.json')
        self.assertTrue( len(fclient._result_suite) == 32 )
        self.assertTrue( len(fclient._failed_result_suite) == 23 )

    # redirect summary support
    def test_export_redirect_summary(self):
        REDIRECT_SUMMARY='redirect_summary.json'
        fclient = FractClient(fract_suite_file='testcase4redirect.json') # includes 7 redirect
        fclient.load_resultfile('result4redirect.json')
        fclient.export_redirect_summary(REDIRECT_SUMMARY)
        
        self.assertTrue( len(fclient.redirect_summary) == 7)
        self.assertTrue( fclient.redirect_summary[0]['Response']['status_code'] == 301 )
        self.assertTrue( fclient.redirect_summary[0]['Response']['Server'] == 'AkamaiGHost' )
        self.assertTrue( fclient.redirect_summary[1]['TestId'] == 'ec5890b017383f077f788478aa41911748e0a5a15b7230a1555b14648950da83' )
        self.assertTrue( 'User-Agent' in fclient.redirect_summary[1]['Request']['Headers'] )
    
    def test_make_spec_summary(self):
        fclient = FractClient(fract_suite_file='testcase4redirect.json') # includes 7 redirect
        fclient.load_resultfile('result4redirect.json')
        fret=fclient._result_suite[0]
        single_summary = fclient._make_spec_summary(fret)

        self.assertTrue( single_summary['Response']['status_code'] == 200 )
        self.assertTrue( single_summary['Response']['Location'] == '' )

    def test_export_ercost_high(self):
        ERCOST_SUMMARY='ercost_high_summary.json'
        fclient = FractClient(fract_suite_file='testcase4redirect.json') # includes 7 redirect
        fclient.load_resultfile('result4redirect.json')
        fclient.export_ercost_high(ERCOST_SUMMARY, 10000000)
        
        self.assertTrue( len(fclient.ercost_high_summary) == 3)


from fract import JsonYaml
class test_JsonYaml(unittest.TestCase):
    def setUp(self):
        self.jy=JsonYaml()
    def tearDown(self):
        pass
    def test_j2y(self):
        self.jy.j2y('testcase4test.json', 'testcase4test.yaml')
    def test_y2j(self):
        self.jy.y2j('testcase4test.yaml', 'testcase4test2.json')


from fract import RedirectLoopTester
class test_RedirectLoopTester(unittest.TestCase):
    def setUp(self):
        self.rlt=RedirectLoopTester()
    def tearDown(self):
        pass

    def test_test_from_urls(self):
        self.rlt.test_from_urls('urllist4redirectloop.txt', 'fract.akamaized-staging.net', 5)
        self.assertTrue( self.rlt.allcount == 10)
        self.assertTrue( self.rlt.errorcount == 4)
        self.assertTrue( self.rlt.hasRedirectCount == 9)
        self.assertTrue( self.rlt.resultList[0]['Threshold'] == 5 )
        self.assertTrue( self.rlt.resultList[0]['ReachedThreshold'] == False )
        self.assertTrue( self.rlt.resultList[0]['URL'] == 'https://fract.akamaized.net/301/3/' )
        self.assertTrue( self.rlt.resultList[0]['TargetHost'] == 'fract.akamaized-staging.net' )
        self.assertTrue( self.rlt.resultList[0]['Depth'] == 3 )

    def test_test_from_urls_2(self):
        self.rlt.test_from_urls('urllist4redirectloop.txt', None, 10)
        self.assertTrue( self.rlt.allcount == 10)
        self.assertTrue( self.rlt.errorcount == 0)
        self.assertTrue( self.rlt.hasRedirectCount == 9)
        self.assertTrue( self.rlt.resultList[0]['Threshold'] == 10 )
        self.assertTrue( self.rlt.resultList[0]['ReachedThreshold'] == False )
        self.assertTrue( self.rlt.resultList[0]['URL'] == 'https://fract.akamaized.net/301/3/' )
        self.assertTrue( self.rlt.resultList[0]['TargetHost'] == 'fract.akamaized.net' )
        self.assertTrue( self.rlt.resultList[0]['Depth'] == 3 )




    def test_tracechain1(self):
        subitem = self.rlt.getNewSubItem()
        self.rlt.tracechain('https://fract.akamaized.net/301/', 'fract.akamaized.net', 5, subitem)
        #logging.warning('test_test_tracechain(): subitem={}'.format(subitem))
        
        self.assertTrue( subitem['Chain'][0]['Location'] == 'https://fract.akamaized.net/' )
        self.assertTrue( subitem['Chain'][0]['status_code'] == 301 )
        
    def test_tracechain2(self):
        testdepth=3
        subitem = self.rlt.getNewSubItem()
        self.rlt.tracechain('https://fract.akamaized.net/301/{}/'.format(testdepth), 'fract.akamaized.net', 5, subitem)
        self.assertTrue( len(subitem['Chain']) == testdepth )
    
    def test_tracechain_overflow(self):
        testdepth=6
        subitem = self.rlt.getNewSubItem()
        self.rlt.tracechain('https://fract.akamaized.net/301/{}/'.format(testdepth), 'fract.akamaized.net', 5, subitem)
        self.assertTrue( len(subitem['Chain']) == 5 )

    def test_tracechain_noredirect(self):
        subitem = self.rlt.getNewSubItem()
        self.rlt.tracechain('https://fract.akamaized.net/', 'fract.akamaized.net', 5, subitem)
        self.assertTrue( len(subitem['Chain']) == 0 )

    def test_save(self):
        pass

    def test_getNewSubItem(self):
        obj = self.rlt.getNewSubItem()
        self.assertTrue('Depth' in obj)
        self.assertTrue('TargetHost' in obj)
        self.assertTrue('Chain' in obj)
        self.assertTrue('Threshold' in obj)
        self.assertTrue( obj['ReachedThreshold'] is False)










if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

