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

from frase import FrakmLog
class test_FrakmLog(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_gen(self):
        fl=FrakmLog()
        fl.gen('www.uniqlo.com', ['topurl.csv', 'topurl2.csv'])
        fl.save('urllist2.txt')


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
        self.assertTrue( 'LoadTime' in ret )
        self.assertTrue( type(ret['LoadTime']) == type(0.1234) )
 
    # custom header support # should be tested through specific ghost conf
    def test_current_stat2(self): 
        fg=FraseGen()
        ret = fg._current_stat('https://amd-ktmrhls41.akamaized.net/hls/live/568564/direct/index.m3u8', 'testnhk-mk.akamaized-staging.net', {'User-Agent': 'iPhone', 'Debug-abc':'foobar' })
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
        cpcode, ttl, ck_host, subdir = fg._parse_xcachekey('L1/L/13100/570226/1d/space.ktmrmshk.com/images/project-image1.jpg cid=___IM_FILE_NAME=.auto.1.2000.chrome&IM_API_TOKEN=space_ktmrmshk_com-10458653&IM_COMB_ON=true')
        self.assertTrue(cpcode == '570226')
        self.assertTrue(ttl == '1d')
        self.assertTrue(ck_host == 'space.ktmrmshk.com')
        self.assertTrue(subdir == 'images')
 
    def test_parse_xcachekey_subdir_support(self):
        fg=FraseGen()
        cpcode, ttl, ck_host, subdir = fg._parse_xcachekey('S/D/13100/570031/000/space.ktmrmshk.com/?akamai-transform=9 cid=___IM_FILE_NAME=.auto')
        self.assertTrue(cpcode == '570031')
        self.assertTrue(ttl == '000')
        self.assertTrue(ck_host == 'space.ktmrmshk.com')
        self.assertTrue(subdir == None)
 
    def test_parse_xcachekey_subdir_support2(self):
        fg=FraseGen()
        cpcode, ttl, ck_host, subdir = fg._parse_xcachekey('S/D/13100/570031/000/space.ktmrmshk.com/ cid=___IM_FILE_NAME=.auto')
        self.assertTrue(cpcode == '570031')
        self.assertTrue(ttl == '000')
        self.assertTrue(ck_host == 'space.ktmrmshk.com')
        self.assertTrue(subdir == None)
 

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
        #self.assertTrue( 'X-Check-Cacheable' in ft.query['TestCase'] )
        
        self.assertTrue( len( ft.query['Comment'] ) != 0 )
        self.assertTrue( len( ft.query['TestId'] ) != 0  )
        self.assertTrue( 'LoadTime' in ft.query )

    # custom_header_support
    def test_gen_20180801(self):
        fg=FraseGen()
        ft = fg.gen('https://space.ktmrmshk.com/','space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net',  {'User-Agent': 'iPhone', 'Debug-abc':'foobar' })
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( ft.query['TestType'] == 'hassert' )
        self.assertTrue( ft.query['Request']['Method'] == 'GET' )
        self.assertTrue( ft.query['Request']['Ghost'] == 'space.ktmrmshk.com.edgekey-staging.net' )
        self.assertTrue( ft.query['Request']['Url'] == 'https://space.ktmrmshk.com/' )
        self.assertTrue( ft.query['Request']['Headers']['User-Agent'] == 'iPhone' )
        self.assertTrue( ft.query['Request']['Headers']['Debug-abc'] == 'foobar' )

        self.assertTrue( 'X-Cache-Key' in ft.query['TestCase'] )
        #self.assertTrue( 'Location' in ft.query['TestCase'] )
        self.assertTrue( 'status_code' in ft.query['TestCase'] )
        self.assertTrue( 'X-Check-Cacheable' in ft.query['TestCase'] )
        
        self.assertTrue( len( ft.query['Comment'] ) != 0 )
        self.assertTrue( len( ft.query['TestId'] ) != 0  )
 

    # Edge redirector cost check support
    def test_gen_20180815_ercost(self):
        fg=FraseGen()
        ft = fg.gen('https://space.ktmrmshk.com/','space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net',  {'User-Agent': 'iPhone', 'Debug-abc':'foobar' })
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( ft.query['TestType'] == 'hassert' )
        self.assertTrue( ft.query['Request']['Method'] == 'GET' )
        self.assertTrue( ft.query['Request']['Ghost'] == 'space.ktmrmshk.com.edgekey-staging.net' )
        self.assertTrue( ft.query['Request']['Url'] == 'https://space.ktmrmshk.com/' )
        self.assertTrue( ft.query['Request']['Headers']['User-Agent'] == 'iPhone' )
        
        self.assertTrue( ft.query['Request']['Headers']['X-Akamai-Cloudlet-Cost'] == 'true' )

    # 2018/08/21 ignore case support
    def test_gen_ignore_case(self):
        fg=FraseGen()
        ft = fg.gen('http://space.ktmrmshk.com/','space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net',  {'User-Agent': 'iPhone', 'Debug-abc':'foobar' }, {'ignore_case':True})
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( ft.query['TestType'] == 'hassert' )
        self.assertTrue( ft.query['Request']['Method'] == 'GET' )
        self.assertTrue( ft.query['Request']['Ghost'] == 'space.ktmrmshk.com.edgekey-staging.net' )
        self.assertTrue( ft.query['Request']['Url'] == 'http://space.ktmrmshk.com/' )
        self.assertTrue( ft.query['Request']['Headers']['User-Agent'] == 'iPhone' )
        self.assertTrue( ft.query['Request']['Headers']['Debug-abc'] == 'foobar' )

        self.assertTrue( 'X-Cache-Key' in ft.query['TestCase'] )
        self.assertTrue( 'Location' in ft.query['TestCase'] )
        self.assertTrue( ft.query['TestCase']['Location'][0]['option']['ignore_case'] == True)
        self.assertTrue( 'status_code' in ft.query['TestCase'] )
        #aself.assertTrue( 'X-Check-Cacheable' in ft.query['TestCase'] )
        
        self.assertTrue( len( ft.query['Comment'] ) != 0 )
        self.assertTrue( len( ft.query['TestId'] ) != 0  )
 
    def test_gen_comment_with_ver_date(self):
        fg=FraseGen()
        ft = fg.gen('https://space.ktmrmshk.com/','space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        
        self.assertTrue( ' at ' in ft.query['Comment'] )

    def test_gen_strict_redirect_cacheability(self):
        fg=FraseGen()
        
        #1 Default => No X-Check-Cacheable when 30x
        ft = fg.gen('https://fract.akamaized.net/301/','fract.akamaized.net', 'fract.akamaized-staging.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertFalse( 'X-Check-Cacheable' in ft.query['TestCase'] )

        #2 strict_redirect_cacheability == True Option => There's  X-Check-Cacheable when 30x
        ft = fg.gen('https://fract.akamaized.net/301/','fract.akamaized.net', 'fract.akamaized-staging.net', mode={'strict_redirect_cacheability': True})
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( 'X-Check-Cacheable' in ft.query['TestCase'] )

        #3 Explicit strict_redirect_cacheability == False Option => No X-Check-Cacheable when 30x
        ft = fg.gen('https://fract.akamaized.net/301/','fract.akamaized.net', 'fract.akamaized-staging.net', mode={'strict_redirect_cacheability': False})
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertFalse( 'X-Check-Cacheable' in ft.query['TestCase'] )


        #4 Default => No X-Check-Cacheable when 302
        ft = fg.gen('https://fract.akamaized.net/302/','fract.akamaized.net', 'fract.akamaized-staging.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertFalse( 'X-Check-Cacheable' in ft.query['TestCase'] )

        #5 Default => No X-Check-Cacheable when 303
        ft = fg.gen('https://fract.akamaized.net/303/','fract.akamaized.net', 'fract.akamaized-staging.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertFalse( 'X-Check-Cacheable' in ft.query['TestCase'] )

        #6 Default => No X-Check-Cacheable when 307
        ft = fg.gen('https://fract.akamaized.net/307/','fract.akamaized.net', 'fract.akamaized-staging.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertFalse( 'X-Check-Cacheable' in ft.query['TestCase'] )

        #7 Default => There's X-Check-Cacheable when NOT 303
        ft = fg.gen('https://fract.akamaized.net/','fract.akamaized.net', 'fract.akamaized-staging.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( 'X-Check-Cacheable' in ft.query['TestCase'] )




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

    # custom header support
    def test_gen_from_urls_20180801(self):
        fg=FraseGen()
        fg.gen_from_urls('urllist4test.txt', 'space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net', {'User-Agent': 'iPhone', 'Debug-abc':'foobar' })
        self.assertTrue( len(fg.testcases) == 32)
        fg.save('out.txt')
        with open('out.txt') as f:
            lines=f.read()
            json_lines=json.loads(lines)
            self.assertTrue( json_lines[0]['Request']['Headers']['User-Agent']=='iPhone')
            self.assertTrue( json_lines[22]['Request']['Headers']['Debug-abc']=='foobar')
    # 2018/08/21 ignore case support
    def test_gen_from_urls_ignore_case(self):
        fg=FraseGen()
        fg.gen_from_urls('urllist4test.txt', 'space.ktmrmshk.com.edgekey.net', 'space.ktmrmshk.com.edgekey-staging.net', option={'ignore_case':True})
        self.assertTrue( len(fg.testcases) == 32)
        fg.save('out.txt')
        with open('out.txt') as f:
            ft=json.load(f)
            self.assertTrue( ft[0]['TestCase']['Location'][0]['option']['ignore_case'] == True)


    def test_gen_from_top_urlog(self):
        fg=FraseGen()
        fg.gen_from_top_urlog('topurl.csv', 'www.uniqlo.com', 'www.uniqlo.com', 'e1753.b.akamaiedge-staging.net')
        fg.save('out.json')

    #2018/11/29 Rum-off Start
    def test_current_rum_off(self):
        logging.info('Start Testing rum off')
        fg=FraseGen()
        ft = fg.gen('https://fract.akamaized.net/mk20xyz/FooBar/example.html', 'fract.akamaized.net', 'fract.akamaized.net', {'Cookie': 'test=123;Test=1234567890'})
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( ft.query['Request']['Headers']['Cookie'] == 'akamai-rum=off;test=123;Test=1234567890' )
        ft = fg.gen('https://fract.akamaized.net/mk20xyz/FooBar/example.html', 'fract.akamaized.net', 'fract.akamaized.net')
        logging.debug('test_case={}'.format(json.dumps(ft.query)))
        self.assertTrue( ft.query['Request']['Headers']['Cookie'] == 'akamai-rum=off' )
        ret = fg._current_stat('https://fract.akamaized.net/mk20xyz/FooBar/example.html', 'fract.akamaized.net', {'Cookie': 'akamai-rum=off;test=123;Test=1234567890'})
        logging.debug('Rum-Off Debug={}'.format(ret))
        self.assertTrue('name=RANDOM_SAMPLE; value=false' in ret['X-Akamai-Session-Info'])
        self.assertTrue(ret['X-Akamai-Transformed'] is '')
        self.assertTrue('"Cookie": "akamai-rum=off;test=123;Test=1234567890"' in ret['Request-Headers'])
        logging.info('rum off testing end')
    #2018/11/29 Rum-off End

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
