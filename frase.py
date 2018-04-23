'''
    Frase: test case generator for Fract
'''

from html.parser import HTMLParser
import requests

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



