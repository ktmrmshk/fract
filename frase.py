'''
    Frase: test case generator for Fract
'''

from html.parser import HTMLParser
import requests
import fract
import logging

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
    Scope of this test case is redirect, CP Code, status_code and TTL
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
        ret['status_code']=r.resh('status_code')
        if r.resh('status_code') in (301, 302, 303, 307): # if redirect response
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

    def gen(self, url, src_ghost, dst_ghost):
        '''
        in: url and ghost
        out: hassert test case
        '''

        ft = fract.FractTestHassert()
        ft.init_template()
        ft.setRequest(url, dst_ghost, {'Pragma':fract.AKAMAI_PRAGMA})

        cstat = self._current_stat(url, src_ghost)
        cpcode, ttl = self._parse_xcachekey(cstat['X-Cache-Key'])
        ft.add('X-Cache-Key', '/{}/'.format(cpcode))
        ft.add('X-Cache-Key', '/{}/'.format(ttl))
        ft.add('X-Check-Cacheable', cstat['X-Check-Cacheable'])
        ft.add('status_code', str(cstat['status_code']) )
        
        if 'Location' in cstat:
            ft.add('Location', cstat['Location'])
            ft.add('status_code', str(cstat['status_code']) )
        return ft

    def _replaceDP(self, logurl, dp):
        '''
        in: logurl: from akamai's top url list. e.g. origin.ktmr.com/jp/css/top-140509.css
        in: dp: digital property or delivery FQDN: like www.ktmr.com
        out: replaced url: like www.ktmr.com/jp/css/top-140509.css
        '''
        
        sp = logurl.split('/')
        sp[0] = dp
        return '/'.join(sp)

    def get_from_akamai_logurl(self, filename, dp, src_ghost, dst_ghost, proto='https://'):
        '''
        in: filename of file that includes list of top url list provided akamai log
        out: None
        process: generate test case and put it into self.testcases
        '''
        cnt=0
        with open(filename) as f:
            for line in f:
                url = proto + self._replaceDP(line, dp)
                tc = self.gen(url, src_ghost, dst_ghost) 
                logging.debug('testcase => {}'.format(tc))
                self.testcases.append( tc )
                cnt+=1
            else:
                logging.debug('FraseGen: testcase generanted: {}'.format(cnt))

    def save(self, filename):
        cnt=0
        with open(filename ,'w') as fw:
            for tc in self.testcases:
                if cnt==0:
                    fw.write('[\n')
                else:
                    fw.write(',\n')
                fw.write('{}'.format(tc))
                cnt+=1
            else:
                fw.write('\n]')

    def load(self, filename):
        pass



