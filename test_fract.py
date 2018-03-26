import unittest, json, logging


from fract import FractTest
class test_FractTest(unittest.TestCase):
    def setUp(self):
        self.fracttest = FractTest()
    def tearDown(self):
        pass
    
    def test_init_template(self):
        self.fracttest.init_template()
        self.assertTrue( 'TestType' in self.fracttest.query )

    def test_init_example_1(self):
        self.fracttest.init_example('hassert')
        self.assertTrue( self.fracttest.query['TestType'] == 'hassert' )
    
    def test_init_example_2(self):
        self.fracttest.init_example('hdiff')
        self.assertTrue( self.fracttest.query['TestType'] == 'hdiff' )

    def test_import_query(self):
        self.fracttest.import_query('''{"TestType":"hassert","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}],"Location":[{"type":"regex","query":"https://www.akamai.com"}]}} ''')
        self.assertTrue( self.fracttest.query['TestType'] == 'hassert' )


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
        self.fractresult.query=json.loads( '''{"TestType":"hassert","Passed":false,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":false,"Value":301,"testcase":{"type":"regex","query":"(200|404)"}},{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":false,"Value":"This Header is not in Response","testcase":{"type":"regex","query":"text/html$"}}]}} ''' )
        ret = self.fractresult.check_passed()
        self.assertTrue( ret == (False, 3, 1, 2) )

    def test_check_passed2(self):
        self.fractresult.query=json.loads('''{"TestType":"hassert","Passed":true,"Response":{"status_code":301,"Content-Length":"0","Location":"https://www.akamai.com","Date":"Mon, 26 Mar 2018 09:20:33 GMT","Connection":"keep-alive","Set-Cookie":"AKA_A2=1; expires=Mon, 26-Mar-2018 10:20:33 GMT; secure; HttpOnly","Referrer-Policy":"same-origin","X-N":"S"},"ResultCase":{"status_code":[{"Passed":true,"Value":301,"testcase":{"type":"regex","query":"301"}}],"Content-Type":[{"Passed":true,"Value":"text/html","testcase":{"type":"regex","query":"text/html$"}}]}}''')
        ret = self.fractresult.check_passed()
        self.assertTrue( ret == (True, 2, 2, 0) )



from fract import Actor
class test_Actor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor()
        self.actor.get('https://space.ktmrmshk.com/abc/example.html?abc=123', ghost='space.ktmrmshk.com.edgekey-staging.net', headers={'Accept-Encoding': 'gzip'})
    def tearDown(self):
        pass

    def test_get(self):
        self.assertTrue( self.actor.r.status_code != 400 )

    def test_get_headers(self):
        self.assertTrue( 'status_code' in self.actor.get_headers() )

    def test_get_status_code(self):
        self.assertTrue( self.actor.get_status_code() == self.actor.r.status_code ) 

    def test_resh(self):
        self.assertTrue( self.actor.resh('status_code') == self.actor.r.status_code )
        self.assertTrue( self.actor.resh('Date') == self.actor.r.headers['Date'] )


from fract import Fract
class test_Fract(unittest.TestCase):
    def setUp(self):
        self.fr = Fract()
    def tearDown(self):
        pass

    def test_run_hassert(self):
        testcase = FractTest()
        testcase.import_query('''{"TestType":"hassert","Request":{"Ghost":"www.akamai.com.edgekey.net","Method":"GET","Url":"https://www.akamai.com/us/en/","Headers":{"Cookie":"abc=123","Accept-Encoding":"gzip"}},"TestCase":{"status_code":[{"type":"regex","query":"(200|404)"},{"type":"regex","query":"301"}],"Content-Type":[{"type":"regex","query":"text/html$"}],"Location":[{"type":"regex","query":"https://www.akamai.com"}]}} ''')
        ret = self.fr._run_hassert(testcase)
        self.assertTrue( ret.query['TestType'] == 'hassert')
        self.assertTrue( ret.query['Passed'] == False )
        logging.info('FractResult: {}'.format(ret))






if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()

