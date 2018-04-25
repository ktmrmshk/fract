import unittest, json, logging

from frase import Htmlpsr
class test_Htmlpsr(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_handle_starttag(self):
        hp=Htmlpsr()
        html='''<!DOCTYPE html><html lang="en"><head> <title>Bootstrap Example</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> <script src="maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> <script src="//example.com/foo.js"></script></head><body><a target="_top" href="bootstrap_filters.asp">BS Filters</a><div class="jumbotron text-center"> <h1>My First Bootstrap Page</h1> <p>Resize this responsive page to see the effect!</p><img src="bs_themes.jpg" style="width:98%;margin:20px 0" alt="Theme Company"></div></body></html>'''
        hp.start(html)
        self.assertTrue( hp.anchors[0] == 'bootstrap_filters.asp')
        self.assertTrue( len(hp.embs) == 5)

from frase import FraseGen
class test_FraseGen(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_current_stat(self):
        fg=FraseGen()
        ret = fg._current_stat('https://amd-ktmrhls41.akamaized.net/hls/live/568564/direct/index.m3u8', 'testnhk-mk.akamaized-staging.net')
        logging.debug('fg.ret={}'.format(ret))
        self.assertTrue(ret['X-Check-Cacheable'] == 'YES')
        self.assertTrue( '544456' in ret['X-Cache-Key'])
    
    def test_current_stat_redirect(self):
        fg=FraseGen()
        ret = fg._current_stat('http://space.ktmrmshk.com', 'space.ktmrmshk.com')
        logging.debug('fg.ret={}'.format(ret))
        self.assertTrue(ret['X-Check-Cacheable'] == 'NO')
        self.assertTrue( '570031' in ret['X-Cache-Key'])
        self.assertTrue(ret['status_code'] == 301)
        self.assertTrue(ret['Location'] == 'https://space.ktmrmshk.com/')


    def test_parse_xcachekey(self):
        fg=FraseGen()
        cpcode, ttl = fg._parse_xcachekey('L1/L/13100/570226/1d/space.ktmrmshk.com/images/project-image1.jpg cid=___IM_FILE_NAME=.auto.1.2000.chrome&IM_API_TOKEN=space_ktmrmshk_com-10458653&IM_COMB_ON=true')
        self.assertTrue(cpcode == '570226')
        self.assertTrue(ttl == '1d')
    
    def test_gen(self):
        fg=FraseGen()
        ft = fg.gen('http://space.ktmrmshk.com/','space.ktmrmshk.com')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( ft.query['Request']['Method'] == 'GET' )
        self.assertTrue( ft.query['Request']['Ghost'] == 'space.ktmrmshk.com' )
        self.assertTrue( ft.query['Request']['Url'] == 'http://space.ktmrmshk.com/' )
        self.assertTrue( 'X-Cache-Key' in ft.query['TestCase'] )
        self.assertTrue( 'Location' in ft.query['TestCase'] )
        self.assertTrue( 'status_code' in ft.query['TestCase'] )
        self.assertTrue( 'X-Check-Cacheable' in ft.query['TestCase'] )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
