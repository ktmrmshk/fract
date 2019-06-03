from fract import *
from frase import *
from frmq import *
from fradb import *
import json, logging, re, time
from config import CONFIG

class FractMan(object):
    def __init__(self):
        self.pub = TaskPublisher()
        self.pub.open()

        self.mj = mongojson()

        self.sessionid=int()
        self.cmd=str()
        '''
        cmd: "testgen", "run"
        '''


    def push(self, filename):
        pass

    def is_queue_empty(self, queuename):
        self.pub.make_queue(queuename)
        return self.pub.get_queue_size(queuename) == 0
        
    def num_task_completed(self):
        return self.mj.count({}, self.cmd, self.sessionid)
        
    def save(self, filename):
        pass

    def clear_taskqueue(self, queuename):
        self.pub.purge(queuename)

class TestGenMan(FractMan):
    def __init__(self, sessionid):
        super(TestGenMan, self).__init__()
        self.cmd="testgen"
        self.sessionid = sessionid
        self.num_task=0

    def push(self, queuename, urllist, src_ghost, dst_ghost, headers={}, options={}, mode={} ):
        '''
        return: size of urllist
    
        msg format
        ---
        testgen message: 
        {
            "cmd": "testgen",
            "sessionid" : 20190430123121,
            "urllist": [
                "https://abc.com/",
                "..."
            ],
            "headers": {
               "User-Agent": "iPhone",
                "Referer": "http://abc.com"
            },
            "options": {
                "ignore_case": true
            },
            "mode": {
                "strict_redirect_cacheability": false
            },
            "src_ghost" : "e13100.a.akamaiedge.net",
            "dst_ghost" : "e13100.a.akamaiedge-staging.net"
        }        
        ---


        '''
        self.pub.make_queue(queuename)
        msg=dict()
        msg['cmd'] = 'testgen'
        msg['sessionid'] = self.sessionid
        msg['urllist'] = urllist
        msg['headers'] = headers
        msg['options'] = options
        msg['src_ghost'] = src_ghost
        msg['dst_ghost'] = dst_ghost
        msg['mode'] = mode

        self.pub.push(queuename, json.dumps(msg))
        self.num_task += len(urllist)


    def split_list(self, l, n):
        '''
        split list 'l' to include 'n' memmber each
        '''
        for i in range(0, len(l), n):
            yield l[i:i+n]


    def push_urllist_from_file(self, filename, chunksize, src_ghost, dst_ghost, headers={}, options={}, mode={}):
        urllist_all=list()
        with open(filename) as f:
            for line in f:
                url=line.strip()
                if url == '':
                    continue
                urllist_all.append(url)
        
        for urllist in self.split_list(urllist_all, chunksize):
            self.push(CONFIG['mq']['queuename'], urllist, src_ghost, dst_ghost, headers={}, options={}, mode={} )


    def save(self, filename, interval=1, timeout_count=5):
        no_diff_count=0
        last_count=0
        while(True):
            num_comp = self.num_task_completed()
            num_task = self.num_task
            if num_comp == num_task:
                self.mj.output(filename, self.cmd, self.sessionid)
                break
            
            if last_count == num_comp:
                no_diff_count+=1
                if no_diff_count > timeout_count:
                    # timeout!
                    print('Timeout')
                    self.mj.output(filename, self.cmd, self.sessionid)
                    break
            else:
                no_diff_count=0
                last_count = num_comp
               
            print('FractMan: waiting results ...{} / {}'.format(num_comp, num_task))
            time.sleep(interval)

  




