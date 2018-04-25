'''
    Frase: test case generator for Fract
'''

from html.parser import HTMLParser
import requests
import fract

class Htmlpsr(HTMLParser):
    def start(self, html):
        self.anchors=list()
        self.embs=list()
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        '''
        pickupt links
        <link rel="apple-touch-icon" href="/jp/img/sp/app_icon.png">
        <script src="/jp/common/js/lib/slick.js"></script>
        <a href="//www.jins.com/jp/st/sunglasses/" class="ss-link linkBtn">
        <img src="/jp/common/img/home/style_men.jpg" width="347" alt="MEN">
        '''
        if tag == 'a':
            for a in attrs:
                if a[0] == 'href':
                    self.anchors.append(a[1])
        elif tag == 'script':
            for a in attrs:
                if a[0] == 'src':
                    self.embs.append(a[1])
        elif tag == 'link':
            for a in attrs:
                if a[0] == 'href':
                    self.embs.append(a[1])
        elif tag == 'img':
            for a in attrs:
                if a[0] == 'src':
                    self.embs.append(a[1])

class Htmlcrwlr(object):
    def __init__(self):
        pass


class FraseGen(object):
    '''
    class to generate HASSERT Test case from existing ghost config.
    Scope of this test case is redirect, CP Code and TTL
    '''
    def __init__(self):
        self.testcases=list()

    def _current_stat(self, url, ghost, headers={}):
        '''
        in: url, ghost, headers
        out: dict of 'x-cache-key', x-cacheable
        '''
        a=fract.Actor()
        headers['Pragma'] = fract.AKAMAI_PRAGMA
        r=a.get(url, headers, ghost)

        ret= {'X-Check-Cacheable':r.resh('X-Check-Cacheable'), 'X-Cache-Key': r.resh('X-Cache-Key')}
        if r.resh('status_code') in (301, 302, 303, 307): # if redirect response
            ret['status_code']=r.resh('status_code')
            ret['Location']=r.resh('Location')
        
        return ret

    def _parse_xcachekey(self, xcachekey_text):
        '''
        in: x-cache-key value like 'L1/L/13100/570226/1d/space.ktmrmshk.com/images/project-image1.jpg cid=___IM_FILE_NAME=.auto.1.2000.chrome&IM_API_TOKEN=space_ktmrmshk_com-10458653&IM_COMB_ON=true'
        out: tupple of (CP Code, TTL)
        '''
        sp = xcachekey_text.split('/')
        ttl = sp[4]
        cpcode = sp[3]
        return (cpcode, ttl)

    def gen(self, url, ghost):
        '''
        in: url and ghost
        out: hassert test case
        '''

        ft = fract.FractTestHassert()
        ft.init_template()
        ft.setRequest(url, ghost, {'Pragma':fract.AKAMAI_PRAGMA})

        cstat = self._current_stat(url, ghost)
        cpcode, ttl = self._parse_xcachekey(cstat['X-Cache-Key'])
        ft.add('X-Cache-Key', '/{}/'.format(cpcode))
        ft.add('X-Cache-Key', '/{}/'.format(ttl))
        ft.add('X-Check-Cacheable', cstat['X-Check-Cacheable'])
        
        if 'Location' in cstat:
            ft.add('Location', cstat['Location'])
            ft.add('status_code', str(cstat['status_code']) )
        
        return ft





