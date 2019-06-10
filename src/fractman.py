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
        
    def num_task_completed(self, session=None):
        if session == None:
            return self.mj.count({}, self.cmd, self.sessionid)
        else:
            return self.mj.count({}, self.cmd, session)
        
    def save(self, filename):
        pass

    def clear_taskqueue(self, queuename):
        self.pub.purge(queuename)

    def split_list(self, l, n):
        '''
        split list 'l' to include 'n' memmber each
        '''
        for i in range(0, len(l), n):
            yield l[i:i+n]




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


    def save(self, filename, interval=1, timeout_count=10000):
        no_diff_count=0
        last_count=0
        while(True):
            num_comp = self.num_task_completed()
            num_task = self.num_task
            if num_comp == num_task:
                self.mj.output(filename, self.cmd, self.sessionid, query={"Active" : { "$not" : {"$eq": False}}})
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

class RunMan(FractMan):
    def __init__(self, sessionid):
        super(RunMan, self).__init__()
        self.cmd="run"
        self.sessionid = sessionid
        self.num_task=0

    def push(self, queuename, testcase_list):
        '''
        testcase_list: list of dict "query" in class FractTest
        return: size of testcase_file
    
        msg format
        ---
        testgen message: 
        {
            "cmd": "run",
            "sessionid" : 20190430123121,
            "testcases" : [{
                "TestType": "hassert",
                "Request": {
                    "Ghost": "e13663.x.akamaiedge-staging.net",
                    "Method": "GET",
                    "Url": "https://www.uniqlo.com/",
                    "Headers": {
                        "Pragma": "akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-check-cacheable,akamai-x-get-cache-key,akamai-x-get-extracted-values,akamai-x-get-request-id,akamai-x-serial-no, akamai-x-get-true-cache-key",
                        "X-Akamai-Cloudlet-Cost": "true",
                        "Cookie": "akamai-rum=off"
                    }
                },
                "TestCase": {
                    "X-Cache-Key": [
                        {
                            "type": "regex",
                            "query": "/27115/"
                        },
                        {
                            "type": "regex",
                            "query": "/30d/"
                        },
                        {
                            "type": "contain",
                            "query": "/orwww.uniqlo.com/"
                        }
                    ],
                    "status_code": [
                        {
                            "type": "regex",
                            "query": "302"
                        }
                    ],
                    "Location": [
                        {
                            "type": "exact",
                            "query": "https://www.uniqlo.com/jp/"
                        }
                    ]
                },
                "Comment": "This test was gened by FraseGen - v0.8 at 2019/06/03, 20:14:16 JST",
                "TestId": "b08307428d6fdd1dcc66ad84762dbfedcc566596e95b21d26d6e58d600f74577",
                "Active": true,
            },
            {
                ...
            }
            ]
        }        
        ---
        '''
        self.pub.make_queue(queuename)
        msg=dict()
        msg['cmd'] = 'run'
        msg['sessionid'] = self.sessionid
        msg['testcases'] = testcase_list
        self.pub.push(queuename, json.dumps(msg))
        self.num_task += len(testcase_list)


    def push_testcase_from_file(self, testcase_file, chunksize):
        fclient = FractClient(fract_suite_file=testcase_file)
        
        for subtestcase_list in self.split_list(fclient._testsuite, chunksize):
            # construct list of raw data (FractClient.query)
            testcases = list()
            for nodetestcase in subtestcase_list:
                testcases.append(nodetestcase.query)
            else:
                self.push(CONFIG['mq']['queuename'], testcases)

    def save(self, result_filename, diff_filename, summary_filename, interval=10):
        fclient = FractClient()
        while(True):
            num_comp = self.num_task_completed(session=self.sessionid)
            num_task = self.num_task
            if num_comp == num_task:
                for suball in self.mj.findall(self.cmd, self.sessionid):
                    fclient._result_suite.append(FractDsetFactory.create(suball))
                for subfail in self.mj.findall(self.cmd, self.sessionid + '_failed'):
                    fclient._failed_result_suite.append(FractDsetFactory.create(subfail))
                fclient.export_result(result_filename)
                fclient.export_failed_testsuite(diff_filename, 'yaml')
                summary = fclient.make_summary()
                print(summary)
                with open(summary_filename, 'w') as fw:
                    fw.write(summary)
                break
            print('FractMan: waiting results ...{} / {}'.format(num_comp, num_task))

            time.sleep(interval)
