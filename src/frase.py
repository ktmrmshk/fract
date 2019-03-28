'''
    Frase: test case generator for Fract
'''

from html.parser import HTMLParser
import requests
import fract
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import urlparse, urljoin
from version import VERSION, strnow


class Htmlpsr(HTMLParser):
    def start(self, html, baseurl, domains=[]):
        '''
        in: html - text
        in: url - text e.g. https://space.ktmrmshk.com/static/img/
        in: domains - list of domain that should be listed, as a filter  e.g. [space.ktmrmshk.com]
        '''
        self.baseurl=baseurl
        self.domains=domains
        self.anchors=dict()
        self.embs=dict()
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
                    self.add_anchors( a[1] )
        elif tag == 'script':
            for a in attrs:
                if a[0] == 'src':
                    self.add_embs( a[1] )
        elif tag == 'link':
            for a in attrs:
                if a[0] == 'href':
                    self.add_embs( a[1] )
        elif tag == 'img':
            for a in attrs:
                if a[0] == 'src':
                    self.add_embs( a[1] )

    def add_embs(self, url):
        fullurl = urljoin(self.baseurl, url)
        if self.domains==[]:
            self.embs[fullurl] = True
        else:
            for d in self.domains:
                if d == urlparse(fullurl).netloc:
                    self.embs[fullurl] = True
                    break

    def add_anchors(self, url):
        fullurl = urljoin(self.baseurl, url)
        if self.domains==[]:
            self.anchors[fullurl] = True
        else:
            for d in self.domains:
                if d == urlparse(fullurl).netloc:
                    self.anchors[fullurl] = True
                    break

    def __str__(self):
        return '{}, {}'.format( self.anchors.__str__(), self.embs.__str__() )


class Htmlcrwlr(object):
    def __init__(self, entrypoint, domains, maxdepth=3):
        '''
        in: entrypoint - url of starting point: 'http://abc.com/jp/'
        in: domains - list of domains for targets
        in: maxdepth - max depth to be parsed over pages

        ---
        anchors is a dict like
        { 'parsed'   : {'http://abc.com/'   : {'depth': 1}, ...}, 
          'unparsed' : {'http://abc.com/jp/': {'depth': 2}, ...}
        }

        '''
        self.hp=Htmlpsr()
        self.urllist = dict()
        self.anchors = {'parsed': dict(), 'unparsed': dict()}
        self.entrypoint= entrypoint
        self.urllist[entrypoint] = True
        self.anchors['unparsed'][entrypoint] = {'depth':0}
        self.domains = domains
        self.maxdepth=maxdepth
        self.a = fract.Actor()

    def __str__(self):
        line=str()
        line+='urllist: total {}\n'.format(len(self.urllist))
        for l in self.urllist:
            line += l + '\n'
        else:
            line += '\n'

        line+='anchors: total {}\n'.format(len(self.anchors['parsed']))
        for k,v in self.anchors['parsed'].items():
            line += '{}, {}\n'.format(k,v)
        else:
            line += '\n'

        return line
        #return 'urllist={}, anchors={}'.format(self.urllist.__str__(), self.anchors.__str__())

    def start(self):
        '''
        breadth first search
        '''
        # pop a anchor url
        url=str()
        stat=dict()
        while len( self.anchors['unparsed'] ) != 0: 
            url, stat = self.anchors['unparsed'].popitem()
            self._scan_singlepage(url, stat)
        return


    def _scan_singlepage(self, url, stat):

        depth=stat['depth']
        # get html
        ret=self.a.get(url)
        logging.debug('request: {} - {}'.format(url, ret.resh('status_code')))

        if ret.resh('status_code') == 200:

            # parse links
            htmltext=ret.r.text
            self.hp.start(htmltext, url, self.domains)

            # append embs link
            for e in self.hp.embs.keys():
                self.urllist[e] = True
        
            # on anchors
            for a in self.hp.anchors.keys():
                if a is url:
                    pass # do nothing
                elif a not in self.anchors['parsed'] and a not in self.anchors['unparsed']:
                    if depth < self.maxdepth:
                        self.anchors['unparsed'][a] = { 'depth': depth+1 }

        elif ret.resh('status_code') in (301, 302, 303, 307):
            # get redirect link
            red_url = urljoin( url, ret.resh('Location') )

            # appdend anchors
            if red_url not in self.anchors['parsed'] and red_url not in self.anchors['unparsed']:
                if depth < self.maxdepth:
                    self.anchors['unparsed'][red_url] = { 'depth': depth+1 }

            # append urllist
            self.urllist[red_url] = True

        else:
            pass

        # append this url to embs link
        self.urllist[url] = True
            
        # update anchors
        if url not in self.anchors['parsed']:
            self.anchors['parsed'][url] = stat

        return 

    def save(self, filename):
        with open(filename, 'w') as fw:
            for u in self.urllist.keys():
                fw.write(u+'\n')
        logging.debug('saved to {}'.format(filename))

class FrakmLog(object):
    '''
    URL List generatetor from logs akamai provides
    '''
    def __init__(self):
        self._urllist=list()

    def gen(self, hostname, logfiles, proto='https://'):
        for logfile in logfiles:
            with open(logfile) as f:
                is_in_url_part=False
                for line in f:
                    if '# ROW_DATA_START' in line:
                        is_in_url_part = True
                        continue
                    elif is_in_url_part:
                        if '# ROW_DATA_END' in line:
                            is_in_url_part=False
                            break
                        # TOP URL
                        urlpart = line.split(',')[0]
                        url = proto + self._replaceDP(urlpart.strip(), hostname)
                        logging.debug('URL => {}'.format(url))
                        self._urllist.append(url)
                    else:
                        pass

    def _replaceDP(self, logurl, dp):
        '''
        in: logurl: from akamai's top url list. e.g. origin.ktmr.com/jp/css/top-140509.css
        in: dp: digital property or delivery FQDN: like www.ktmr.com
        out: replaced url: like www.ktmr.com/jp/css/top-140509.css
        '''
        
        sp = logurl.split('/')
        sp[0] = dp
        return '/'.join(sp)



    def save(self, filename):
        with open(filename, 'w') as f:
            for u in self._urllist:
                f.write(u+'\n')
        logging.debug('saved to {}'.format(filename))



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
        #2018/11/29 Rum-off Start
        ret['Request-Headers'] = r.resh('Request-Headers')
        ret['X-Akamai-Session-Info'] = r.resh('X-Akamai-Session-Info')
        ret['X-Akamai-Transformed'] = r.resh('X-Akamai-Transformed')
        #2018/11/29 Rum-off End
        
        return ret

    def _parse_xcachekey(self, xcachekey_text):
        '''
        in: x-cache-key value like 'L1/L/13100/570226/1d/space.ktmrmshk.com/images/project-image1.jpg cid=___IM_FILE_NAME=.auto.1.2000.chrome&IM_API_TOKEN=space_ktmrmshk_com-10458653&IM_COMB_ON=true'
        out: tupple of (CP Code, TTL)
        '''
        sp = xcachekey_text.split('/')
        ttl = sp[4]
        cpcode = sp[3]
        ck_host = sp[5]
        subdir = None
        if len(sp) > 6:
            if not sp[6].strip().startswith('cid=') and not sp[6].strip().startswith('?'):
                subdir=sp[6]
        return (cpcode, ttl, ck_host, subdir)

    def gen(self, url, src_ghost, dst_ghost, headers={}, option={}):
        '''
        in: url and ghost
        out: hassert test case
        '''

        ft = fract.FractTestHassert()
        ft.init_template()
        headers.update({'Pragma':fract.AKAMAI_PRAGMA})
        headers.update({'X-Akamai-Cloudlet-Cost': 'true'})
        #2018/11/29 Rum-off Start
        cookieFromCustomer = headers.get('Cookie', '')
        if 'akamai-rum=off' not in cookieFromCustomer:
            if cookieFromCustomer is '':
                headers.update({'Cookie': 'akamai-rum=off'})
            else:
                headers.update({'Cookie': 'akamai-rum=off;' + cookieFromCustomer})
        #2018/11/29 Rum-off End
        ft.setRequest(url, dst_ghost, headers)
        
        cstat = self._current_stat(url, src_ghost, headers)
        cpcode, ttl, ck_host, subdir = self._parse_xcachekey(cstat['X-Cache-Key'])
        
        ft.add('X-Cache-Key', '/{}/'.format(cpcode), option=option)
        ft.add('X-Cache-Key', '/{}/'.format(ttl), option=option)
        if subdir:
            ft.add('X-Cache-Key', '/{}/{}'.format(ck_host, subdir), 'contain', option=option)
        else:
            ft.add('X-Cache-Key', '/{}/'.format(ck_host), 'contain', option=option)
        
        ft.add('X-Check-Cacheable', cstat['X-Check-Cacheable'], option=option)
        ft.add('status_code', str(cstat['status_code']), option=option)
        ft.set_comment('This test was gened by FraseGen - {} at {}'.format(VERSION, strnow()))
        ft.set_testid()
        if 'Location' in cstat:
            ft.add('Location', cstat['Location'], 'exact', option=option)
            #ft.add('status_code', str(cstat['status_code']) )
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
                url = proto + self._replaceDP(line.strip(), dp)
                tc = self.gen(url, src_ghost, dst_ghost) 
                logging.debug('testcase => {}'.format(tc))
                self.testcases.append( tc )
                cnt+=1
            else:
                logging.debug('FraseGen: testcase generanted: {}'.format(cnt))

    def gen_from_urls(self, filename, src_ghost, dst_ghost, headers={}, option={}):
        cnt=0
        with open(filename) as f:
            for line in f:
                url=line.strip()
                if url == '':
                    continue
                try:
                    tc = self.gen(url, src_ghost, dst_ghost, headers, option)
                    self.testcases.append( tc )
                    cnt+=1
                except Exception as e:
                    logging.warning(e)
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


    def gen_from_top_urlog(self, csvfile, dp, src_ghost, dst_ghost, proto='https://'):
        '''
        in: csvfile - akamai's log containing top 500 urls
        '''
        is_in_url_part=False
        with open(csvfile) as f:
            for line in f:
                if '# ROW_DATA_START' in line:
                    is_in_url_part = True
                    continue
                elif is_in_url_part:
                    if '# ROW_DATA_END' in line:
                        is_in_url_part=False
                        break
                    # TOP URL
                    urlpart = line.split(',')[0]
                    url = proto + self._replaceDP(urlpart.strip(), dp)
                    tc = self.gen(url, src_ghost, dst_ghost)
                    logging.debug('testcase => {}'.format(tc))
                    self.testcases.append( tc )
                else:
                    pass

