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
        hp.start(html, 'http://example.com/')
        self.assertTrue( 'http://example.com/bootstrap_filters.asp' in hp.anchors  )
        self.assertTrue( len(hp.embs) == 5)
 
    def test_handle_start_nonfilter(self):
        example_html = str()
        with open('example.html') as f:
            example_html = f.read()
        hp=Htmlpsr()
        hp.start(example_html, 'http://www.uniqlo.com/jp/')
        self.assertTrue( hp.embs['http://www.uniqlo.com/jp/css/uniqlo.css']  )
        self.assertTrue( hp.embs['http://www.uniqlo.com/jp/js/top_rollover.js']  )
        self.assertTrue( hp.embs['http://www.uniqlo.com/jp/js/top_rollover.js']  )
        self.assertTrue( hp.embs['http://service.maxymiser.net/cdn/uniqlo/desktop-jp/js/mmcore.js'] )
        self.assertTrue( hp.embs['https://im.uniqlo.com/images/jp/pc/img/material/nav/btn_nav_global_001_UQ_JP.gif'] )
        
        self.assertTrue( hp.anchors['http://www.uniqlo.com/jp/store/feature/uq/new/kids/'] )
        self.assertTrue( hp.anchors['http://utme.uniqlo.com/?locale=ja&utm_medium=pc_l1&utm_source=pc_l1&utm_campaign=utme'] )
        self.assertTrue( hp.anchors['http://www.gu-japan.com/?utm_source=uq&utm_medium=refarral'] )
        
        showstr='anchors: total {}\n'.format(len(hp.anchors))
        for l in hp.anchors.keys():
            showstr += l + '\n'
        else:
            logging.debug( showstr )

        showstr='embs: total {}\n'.format(len(hp.embs))
        for l in hp.embs.keys():
            showstr += l + '\n'
        else:
            logging.debug( showstr )

        


    def test_handle_start_filtered(self):
        example_html = str()
        with open('example.html') as f:
            example_html = f.read()
        hp=Htmlpsr()
        hp.start(example_html, 'http://www.uniqlo.com/jp/', ['www.uniqlo.com', 'im.uniqlo.com'])
        self.assertTrue( hp.embs['http://www.uniqlo.com/jp/css/uniqlo.css']  )
        self.assertTrue( hp.embs['http://www.uniqlo.com/jp/js/top_rollover.js']  )
        self.assertTrue( hp.embs['http://www.uniqlo.com/jp/js/top_rollover.js']  )
        self.assertTrue( 'http://service.maxymiser.net/cdn/uniqlo/desktop-jp/js/mmcore.js' not in hp.embs )
        self.assertTrue( hp.embs['https://im.uniqlo.com/images/jp/pc/img/material/nav/btn_nav_global_001_UQ_JP.gif'] )

        self.assertTrue( hp.anchors['http://www.uniqlo.com/jp/store/feature/uq/new/kids/'] )
        self.assertTrue( 'http://utme.uniqlo.com/?locale=ja&utm_medium=pc_l1&utm_source=pc_l1&utm_campaign=utme' not in hp.anchors )
        self.assertTrue( 'http://www.gu-japan.com/?utm_source=uq&utm_medium=refarral' not in hp.anchors )


from frase import Htmlcrwlr
class test_Htmlcrwlr(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_init(self):
        hc = Htmlcrwlr('http://www.abc.com/jp/', ['www.abc.com'])
        self.assertTrue( hc.entrypoint == 'http://www.abc.com/jp/' )
        self.assertTrue( hc.urllist['http://www.abc.com/jp/'] )
        self.assertTrue( hc.anchors == {'parsed': {}, 'unparsed': {'http://www.abc.com/jp/': {'depth': 0}}} )
        self.assertTrue( hc.maxdepth == 3)

    def test_scan_singlepage_1(self):
        hc = Htmlcrwlr('http://space.ktmrmshk.com/', ['space.ktmrmshk.com'])
        
        hc._scan_singlepage('http://space.ktmrmshk.com/', {'depth': 0})
        logging.warning(hc)
        
        self.assertTrue( hc.urllist['http://space.ktmrmshk.com/'] )
        self.assertTrue( hc.urllist['https://space.ktmrmshk.com/'] )
        self.assertTrue( hc.anchors['parsed']['http://space.ktmrmshk.com/'] == {'depth' : 0} )
        self.assertTrue( hc.anchors['unparsed']['https://space.ktmrmshk.com/'] == {'depth' : 1} )

    def test_start1(self):
        hc = Htmlcrwlr('http://space.ktmrmshk.com/', ['space.ktmrmshk.com'], 1)
        hc.start()
        logging.warning(hc)
        
        self.assertTrue( hc.urllist['http://space.ktmrmshk.com/'] )
        self.assertTrue( hc.urllist['https://space.ktmrmshk.com/'] )
        self.assertTrue( hc.urllist['https://space.ktmrmshk.com/images/project-image3.jpg'] )
        self.assertTrue( hc.urllist['https://space.ktmrmshk.com/js/mobile.js'] )
  
    def test_start2(self):
        hc = Htmlcrwlr('http://space.ktmrmshk.com/', ['space.ktmrmshk.com'], 10)
        hc.start()
        
        self.assertTrue( hc.urllist['http://space.ktmrmshk.com/'] )
        self.assertTrue( hc.urllist['https://space.ktmrmshk.com/'] )
        self.assertTrue( hc.urllist['https://space.ktmrmshk.com/images/project-image3.jpg'] )
        self.assertTrue( hc.urllist['https://space.ktmrmshk.com/js/mobile.js'] )
    
        logging.warning(hc)

        
    def test_start3(self):
        hc = Htmlcrwlr('http://www.uniqlo.com/', ['www.uniqlo.com'], 1)
        hc.start()
        logging.warning(hc)


        

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
        ft = fg.gen('http://space.ktmrmshk.com/','space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( ft.query['TestType'] == 'hassert' )
        self.assertTrue( ft.query['Request']['Method'] == 'GET' )
        self.assertTrue( ft.query['Request']['Ghost'] == 'space.ktmrmshk.com.edgekey-staging.net' )
        self.assertTrue( ft.query['Request']['Url'] == 'http://space.ktmrmshk.com/' )
        self.assertTrue( 'X-Cache-Key' in ft.query['TestCase'] )
        self.assertTrue( 'Location' in ft.query['TestCase'] )
        self.assertTrue( 'status_code' in ft.query['TestCase'] )
        self.assertTrue( 'X-Check-Cacheable' in ft.query['TestCase'] )
        
        self.assertTrue( len( ft.query['Comment'] ) != 0 )
        self.assertTrue( len( ft.query['TestId'] ) != 0  )

    def test_replaceDP(self):
        fg=FraseGen()
        ret=fg._replaceDP('origin.ktmr.com/jp/css/top-140509.css', 'www.ktmr.com')
        self.assertTrue( ret == 'www.ktmr.com/jp/css/top-140509.css')

    def test_get_from_akamai_logurl(self):
        fg=FraseGen()
        fg.get_from_akamai_logurl('testurls.csv', 'www.uniqlo.com', 'www.uniqlo.com', 'e1753.b.akamaiedge-staging.net')
        self.assertTrue( len(fg.testcases) == 30)
        fg.save('out.txt')

    def test_gen_from_urls(self):
        fg=FraseGen()
        fg.gen_from_urls('urllist4test.txt', 'space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net')
        self.assertTrue( len(fg.testcases) == 32)
        fg.save('out.txt')



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
