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
        self.fractresult.query=json.loads( '''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":false,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":false,"Value":301,"testcase":{"type":"regex","query":"(200|404)"}},{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":false,"Value":"This Header is not in Response","testcase":{"type":"regex","query":"text/html$"}}]}} ''' )
        ret = self.fractresult.check_passed()
        self.assertTrue( ret == (False, 3, 1, 2) )

    def test_check_passed2(self):
        self.fractresult.query=json.loads('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":true,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":true,"Value":"text/html","testcase":{"type":"regex","query":"text/html$"}}]}}''')
        ret = self.fractresult.check_passed()
        self.assertTrue( ret == (True, 2, 2, 0) )

    def test_str_resultcase(self):
        self.fractresult.query=json.loads('''{"TestType":"hassert","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","Passed":true,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":true,"Value":"text/html","testcase":{"type":"regex","query":"text/html$"}}]}}''')
        ret=self.fractresult._str_resultcase( True )
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
        self.actorresponse = self.actor.get('https://space.ktmrmshk.com/abc/example.html?abc=123', ghost='space.ktmrmshk.com.edgekey-staging.net', headers={'Accept-Encoding': 'gzip'})
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

    def test_siggleton(self):
        a = Actor()
        b = Actor()
        self.assertTrue( a == b)

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

    def test_check_headercase(self):
        ret = self.fr._check_headercase('status_code', [{"type":"regex","query":"301"}], {'status_code': 301})
        self.assertTrue( ret[0]['Passed'] == True )
        self.assertTrue( ret[0]['Value'] == 301 )
        self.assertTrue( ret[0]['testcase']['type'] == 'regex' )


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
        logging.info('FractResult: {}'.format(ret))
        
    def test_run2(self):
        testcase = FractTest()
        testcase.import_query('''{"TestType":"hdiff","Comment":"This is a test for redirect","TestId":"3606bd5770167eaca08586a8c77d05e6ed076899","RequestA":{"Ghost":"www.akamai.com","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"RequestB":{"Ghost":"www.akamai.com.edgekey-staging.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"VerifyHeaders":["Last-Modified","Cache-Control", "status_code", "Content-Length"]} ''')
        fr =Fract()
        ret = fr.run(testcase)
        logging.warning('fractresult= {}'.format(ret))
        self.assertTrue( ret.query['TestType'] == 'hdiff')


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



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

