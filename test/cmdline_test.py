import unittest, logging, argparse, os, datetime, subprocess, shlex, json, glob
from pathlib import Path
from datetime import datetime

basePath = os.path.abspath(os.path.dirname(__file__))


totalLogs = ''
fraui_path = '"' + os.path.join(Path(basePath).parent, 'src/fraui.py') + '"'
envpathout = os.path.join(basePath, 'cmdline_test_output')
envpathin = os.path.join(basePath,'cmdline_test_input')

if not os.path.isdir(envpathout):
    os.mkdir(envpathout)
if not os.path.isdir(envpathin):
    os.mkdir(envpathin)

class testFractCommnand(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fraui_path = fraui_path
        self.COMMAND = ''
        self.HOMEPAGE_URL = 'https://fract.akamaized.net/'
        self.CSS_URL = 'https://fract.akamaized.net/css/main.css'
        self.TESTHOST = 'fract.akamaized.net'
        self.TESTHOST_STAGING = 'fract.akamaized-staging.net'
        self.URLLIST = '"' + os.path.join(envpathout, 'urllist.txt') + '"'
        self.TOPURLLIST = '"' + os.path.join(envpathin, 'fract.akamaized.net_urls.csv') + '"'
        self.TESTCASE = '"' + os.path.join(envpathout, 'testcase.json') + '"'
        self.URLLIST_FORINPUT = '"' + os.path.join(envpathin, 'urllist_for_input.txt') + '"'
        self.DIFFYAML = '"' + os.path.join(envpathin, 'frdiff_test.yaml') + '"'
        self.DIFFJSON = '"' + os.path.join(envpathout, 'frdiff_test.json') + '"'
        self.FINAL_SUMMARY = '"' + os.path.join(envpathout, 'final_summary.txt') + '"'
        self.FINAL_RESULT = '"' + os.path.join(envpathout, 'final_result.json') + '"'
        self.FINAL_TESTCASE = '"' + os.path.join(envpathout, 'final_testcase.json') + '"'
        self.RUN_TEST_FIRST_OUTPUT = '"' + os.path.join(envpathout, 'fret_first.json') + '"'
        self.RUN_TEST_FIRST_DIFF = '"' + os.path.join(envpathout, 'frdiff_first.yaml') + '"'
        self.RUN_TEST_FIRST_SUMMARY = '"' + os.path.join(envpathout, 'frsummary_first.json') + '"'
        self.RUN_TEST_SECOND_OUTPUT = '"' + os.path.join(envpathout, 'fret_second.json') + '"'
        self.RUN_TEST_SECOND_DIFF = '"' + os.path.join(envpathout, 'frdiff_second.yaml') + '"'
        self.RUN_TEST_SECOND_SUMMARY = '"' + os.path.join(envpathout, 'frsummary_second.json') + '"'
        self.MERGE_TESTCASE_1 = '"' + os.path.join(envpathin, 'testcase_formerge1.json') + '"'
        self.MERGE_TESTCASE_2 = '"' + os.path.join(envpathin, 'testcase_formerge2.json') + '"'
        self.MERGE_TESTCASE_FINAL = '"' + os.path.join(envpathout, 'final_testcase.json') + '"'
        self.TESTCASE_REDIRECTION = '"' + os.path.join(envpathin, 'testcase_redirection.json') + '"'
        self.REDIRECTION_RESULT = '"' + os.path.join(envpathin, 'redirection_result.json') + '"'
        self.REDIRECTION_SUMMARY = '"' + os.path.join(envpathout, 'redirection_summary.json') + '"'
        ### 2019/04/08 testredirectloop start
        self.REDIRECTLOOP_INPUT = '"' + os.path.join(envpathin, 'looplist.txt') + '"'
        self.REDIRECTLOOP_RESULT = '"' + os.path.join(envpathout, 'loopresult.json') + '"'
        self.REDIRECTLOOP_SUMMARY = '"' + os.path.join(envpathout, 'loopsummary.txt') + '"'
        ### 2019/04/08 testredirectloop end

        logging.debug('remove output files')
        if (os.path.isfile(self.URLLIST)):
            os.remove(self.URLLIST)
        if (os.path.isfile(self.TESTCASE)):
            os.remove(self.TESTCASE)
        if (os.path.isfile(self.DIFFJSON)):
            os.remove(self.DIFFJSON)
        if (os.path.isfile(self.FINAL_SUMMARY)):
            os.remove(self.FINAL_SUMMARY)
        if (os.path.isfile(self.FINAL_RESULT)):
            os.remove(self.FINAL_RESULT)
        for i in self.getTestResultsFiles(self, basePath):
            os.remove(i)
        for i in self.getTestResultsFiles(self, envpathout):
            os.remove(i)
        if (os.path.isfile(self.MERGE_TESTCASE_FINAL)):
            os.remove(self.MERGE_TESTCASE_FINAL)
        if (os.path.isfile(self.REDIRECTION_RESULT)):
            os.remove(self.REDIRECTION_RESULT)
        if (os.path.isfile(self.REDIRECTION_SUMMARY)):
            os.remove(self.REDIRECTION_SUMMARY)
        ### 2019/04/08 testredirectloop start
        if (os.path.isfile(self.REDIRECTLOOP_RESULT)):
            os.remove(self.REDIRECTLOOP_RESULT)
        if (os.path.isfile(self.REDIRECTLOOP_SUMMARY)):
            os.remove(self.REDIRECTLOOP_SUMMARY)
        ### 2019/04/08 testredirectloop end

    @classmethod
    def tearDownClass(self):
        pass

    def do_cmd(self, cmd):
        '''
        cmd: command line string i.e. 'fract run -h'
        '''
        logging.debug('cmd => {}'.format(cmd))
        cmd_list = shlex.split(cmd)
        return subprocess.run(cmd_list, stdout=subprocess.PIPE)
    
    def getTestResultsFiles(self, tmpPath):
        '''
        get files: frdiff*.yaml fret*.json frsummary*.txt
        '''
        logging.info('getting frdiff*.yaml fret*.json frsummary*.txt')
        listyaml = glob.glob(os.path.join(tmpPath, r'frdiff*.yaml'))
        listjson = glob.glob(os.path.join(tmpPath, r'fret*.json'))
        listtxt = glob.glob(os.path.join(tmpPath, r'frsummary*.txt'))
        listResult = listyaml + listjson + listtxt
        return listResult

    def test_HelpInformation(self):
        '''
        Scenario
        1. run commmand the same as fract -h
        2. check help informtaion output
        '''
        logging.info('Testing: Help Information Output')
        self.COMMAND = 'python3 {}'.format(fraui_path)
        result = self.do_cmd(self.COMMAND)
        stdout_org = result.stdout.decode('utf-8')
        self.assertIn('usage: fract [-h] [-v]', stdout_org)

    def test_GetURLc(self):
        '''
        Scenario
        1. run commmand the same as fract geturlc -e https://fract.akamaized.net -d 1 -o urllist.txt -D fract.akamaized.net
        2. check if https://fract.akamaized.net/css/main.css in urllist.txt
        '''
        logging.info('Testing: URL generation')
        self.COMMAND = 'python3 {} geturlc -e {} -d 1 -o {} -D {}'.format(fraui_path, self.HOMEPAGE_URL, self.URLLIST, self.TESTHOST)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.URLLIST.strip('"')))
        if os.path.isfile(self.URLLIST):
            with open(self.URLLIST, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index(self.CSS_URL) > 0)

    def test_GetURLcFromCSV(self):
        '''
        Scenario
        1. run commmand the same as fract geturlakm -i fract.akamaized.net_urls.csv -D 'fract.akamaized.net' -p https -o urllist.txt
        2. check if https://fract.akamaized.net/css/main.css in urllist.txt
        '''
        logging.info('Testing: URL generation by Akamai top url')
        self.COMMAND = 'python3 {} geturlakm -i {} -D {} -p https -o {}'.format(fraui_path, self.TOPURLLIST, self.TESTHOST, self.URLLIST)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.URLLIST.strip('"')))
        if os.path.isfile(self.URLLIST):
            with open(self.URLLIST, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index(self.CSS_URL) > 0)

    def test_Maketestcases(self):
        '''
        Scenario
        1. run commmand the same as $ fract -v testgen -i urllist_for_input.txt -o testcase.json -s fract.akamaized.net -d fract.akamaized-staging.net
        2. check if test case for https://fract.akamaized.net/css/main.css exists.
        '''
        logging.info('Testing: Making test cases by urllist.txt')
        self.COMMAND = 'python3 {} -v testgen -i {} -o {} -s {} -d {}'.format(fraui_path, self.URLLIST_FORINPUT, self.TESTCASE, self.TESTHOST, self.TESTHOST_STAGING)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.TESTCASE.strip('"')))
        if os.path.isfile(self.TESTCASE):
            with open(self.TESTCASE, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('{"TestType": "hassert", "Request": {"Ghost": "fract.akamaized-staging.net", "Method": "GET", "Url": "https://fract.akamaized.net/css/main.css", "Headers": {"Pragma": "akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-check-cacheable,akamai-x-get-cache-key,akamai-x-get-extracted-values,akamai-x-get-request-id,akamai-x-serial-no, akamai-x-get-true-cache-key"}}, "TestCase": {"X-Cache-Key": [{"type": "regex", "query": "/728260/"}, {"type": "regex", "query": "/1d/"}], "X-Check-Cacheable": [{"type": "regex", "query": "YES"}], "status_code": [{"type": "regex", "query": "200"}]}, "Comment": "This test was gened by FraseGen"') > 0)

    def test_MaketestcasesWithAddtionalHeader(self):
        '''
        Scenario
        1. run commmand the same as $ fract -v testgen -H '{"User-Agent": "iPhone", "Referer": "http://www.abc.com/"}' -i urllist_for_input.txt -o testcase.json -s fract.akamaized.net -d fract.akamaized-staging.net
        2. check if test case for https://fract.akamaized.net/css/main.css exists.
        '''
        logging.info('Testing: Making test cases by urllist.txt')
        self.COMMAND = 'python3 {} -v testgen -H {} -i {} -o {} -s {} -d {}'.format(fraui_path, '\'{"User-Agent": "iPhone", "Referer": "http://www.abc.com/"}\'', self.URLLIST_FORINPUT, self.TESTCASE, self.TESTHOST, self.TESTHOST_STAGING)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.TESTCASE.strip('"')))
        if os.path.isfile(self.TESTCASE):
            with open(self.TESTCASE, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('"Headers": {"User-Agent": "iPhone", "Referer": "http://www.abc.com/", "Pragma": "akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-check-cacheable,akamai-x-get-cache-key,akamai-x-get-extracted-values,akamai-x-get-request-id,akamai-x-serial-no, akamai-x-get-true-cache-key", "X-Akamai-Cloudlet-Cost": "true"}}') > 0)

    def test_RunTestcases(self):
        '''
        Scenario
        1. run commmand the same as $ fract -v run -i testcase.json
        2. check if frdiff*.yaml fret*.json frsummary*.txt three files exist.
        '''
        logging.info('Testing: Run testcases')
        self.COMMAND = 'python3 {} -v run -i {}'.format(fraui_path, self.TESTCASE)
        now = datetime.today()
        midstart = int(now.strftime('%Y%m%d%H%M%S%f'))
        self.do_cmd(self.COMMAND)
        now = datetime.today()
        midafter = int(now.strftime('%Y%m%d%H%M%S%f'))
        listResult = self.getTestResultsFiles(basePath)
        filecount = 0
        for i in listResult:
            tmpFilename = os.path.basename(i).split('.')[0]
            logging.debug('Filename except extension: ' + tmpFilename)
            if 'frdiff' in tmpFilename:
                tmpID = int(tmpFilename[6:])
                if tmpID < midafter and tmpID > midstart:
                    filecount += 1
                    with open(i, mode='r') as rf:
                        contents = rf.read()
                        self.assertTrue(contents.index('Ghost: fract.akamaized-staging.net') > 0)
            if 'fret' in tmpFilename:
                tmpID = int(tmpFilename[4:])
                if tmpID < midafter and tmpID > midstart:
                    filecount += 1
                    with open(i, mode='r') as rf:
                        contents = rf.read()
                        self.assertTrue(contents.index('X-Akamai-Session-Info') > 0)
            if 'frsummary' in tmpFilename:
                tmpID = int(tmpFilename[9:])
                if tmpID < midafter and tmpID > midstart:
                    filecount += 1
                    with open(i, mode='r') as rf:
                        contents = rf.read()
                        self.assertTrue(contents.index('Summary') > 0)
        self.assertTrue(filecount == 3)

    def test_Y2J(self):
        '''
        Scenario
        1. run commmand the same as $ fract y2j frdiff_test.yaml frdiff_test.josn
        '''
        logging.info('Testing: Y2J')
        self.COMMAND = 'python3 {} y2j {} {}'.format(fraui_path, self.DIFFYAML, self.DIFFJSON)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.DIFFJSON.strip('"')))
        if os.path.isfile(self.DIFFJSON):
            with open(self.DIFFJSON, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('"query": "302"') > 0)

    def test_MergeResults(self):
        '''
        Scenario
        1. run command the same as $ fract rmerge -t testcase.json frdiff*.json -r fret* -s final_summary.txt -o final_result.json
        '''
        logging.info('Testing: Merge Results')
        #first step : testcase.json
        self.COMMAND = 'python3 {} -v run -i {} -o {} -s {} -d {}'.format(fraui_path, self.TESTCASE, self.RUN_TEST_FIRST_OUTPUT, self.RUN_TEST_FIRST_SUMMARY, self.RUN_TEST_FIRST_DIFF)
        self.do_cmd(self.COMMAND)
        #second step : frdiff_test.json
        self.COMMAND = 'python3 {} -v run -i {} -o {} -s {} -d {}'.format(fraui_path, self.DIFFJSON, self.RUN_TEST_SECOND_OUTPUT, self.RUN_TEST_SECOND_SUMMARY, self.RUN_TEST_SECOND_DIFF)
        self.do_cmd(self.COMMAND)
        #merge
        self.COMMAND = 'python3 {} rmerge -t {} {} -r {} {} -s {} -o {}'.format(fraui_path, self.TESTCASE, self.DIFFJSON, self.RUN_TEST_FIRST_OUTPUT, self.RUN_TEST_SECOND_OUTPUT, self.FINAL_SUMMARY, self.FINAL_RESULT)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.FINAL_SUMMARY.strip('"')))
        self.assertTrue(os.path.isfile(self.FINAL_RESULT.strip('"')))

    def test_MergeTestCases(self):
        '''
        Scenario
        1. run command the same as $ fract tmerge -t testcase_formerge1.json testcase_formerge2.json -o final_testcase.json
        '''
        logging.info('Testing: Merge Testcases')
        #merge
        self.COMMAND = 'python3 {} tmerge -t {} {} -o {}'.format(fraui_path, self.MERGE_TESTCASE_1, self.MERGE_TESTCASE_2, self.FINAL_TESTCASE)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.FINAL_TESTCASE.strip('"')))
        if os.path.isfile(self.FINAL_TESTCASE):
            with open(self.FINAL_TESTCASE, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('http://space.ktmrmshk.com/') > 0)

    def test_ExportRedirectSummary(self):
        '''
        Scenario
        1. run command the same as $ fract redirsum -t testcase_redirect.json -r result_redirect.json -o summary_redirect.json
        '''
        logging.info('Testing: Export Redirect Summary')
        #make result_redirect.json
        self.COMMAND = 'python3 {} -v run -i {} -o {}'.format(fraui_path, self.TESTCASE_REDIRECTION, self.REDIRECTION_RESULT)
        self.do_cmd(self.COMMAND)
        #redirsum
        self.COMMAND = 'python3 {} redirsum -t {} -r {} -o {}'.format(fraui_path, self.TESTCASE_REDIRECTION, self.REDIRECTION_RESULT, self.REDIRECTION_SUMMARY)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.REDIRECTION_RESULT.strip('"')))
        self.assertTrue(os.path.isfile(self.REDIRECTION_SUMMARY.strip('"')))
        #if os.path.isfile(self.REDIRECTION_SUMMARY):
        #    with open(self.REDIRECTION_SUMMARY, mode='r') as rf:
        #        contents = rf.read()
        #        self.assertTrue(contents.index('http://space.ktmrmshk.com/') > 0)

    ### 2019/04/08 testredirectloop start
    def test_RedirectLoop(self):
        '''
        Scenario
        1. run command the same as $ fract testredirectloop -i looplist.txt -o loopsummary.txt -r loopresult.json -s fract.akamaized.net -m 3
        '''
        logging.info('Testing: Export Redirect Summary')
        self.COMMAND = 'python3 {} -v testredirectloop -i {} -o {} -r {} -s {} -m {}'.format(fraui_path, self.REDIRECTLOOP_INPUT, self.REDIRECTLOOP_SUMMARY, self.REDIRECTLOOP_RESULT, "fract.akamaized.net", 3)
        self.do_cmd(self.COMMAND)
        self.assertTrue(os.path.isfile(self.REDIRECTLOOP_RESULT.strip('"')))
        self.assertTrue(os.path.isfile(self.REDIRECTLOOP_SUMMARY.strip('"')))
        if os.path.isfile(self.REDIRECTLOOP_SUMMARY):
            with open(self.REDIRECTLOOP_SUMMARY, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('Maximum Value 3') > 0)
        if os.path.isfile(self.REDIRECTION_RESULT):
            with open(self.REDIRECTION_RESULT, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('MaximumValue') > 0)
                self.assertTrue(contents.index('Depth') > 0)
                self.assertTrue(contents.index('301') > 0)
                self.assertTrue(contents.index('302') > 0)
                self.assertTrue(contents.index('303') > 0)
                self.assertTrue(contents.index('307') > 0)
    ### 2019/04/08 testredirectloop end


# edge redirector cost check support
class testERCost(unittest.TestCase):
    def setUp(self):
        self.URLLIST='urllist.txt.test'
        self.TESTCASE='testcase.json.test'
        self.RESULT='result.json.test'
        self.SUMMARY='summary.txt.test'
        self.TDIFF='testdiff.yaml.test'
        self.REDIRECT_SUMMARY='redirect_summary.json.test'
        self.ERCOST_SUMMARY='ercost_summary.json.test'

        cmd='rm *.test'
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    def tearDown(self):
        #  remove files
        cmd='rm *.test'
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    def do_cmd(self, cmd):
        '''
        cmd: command line string i.e. 'fract run -h'
        '''
        logging.debug('cmd => {}'.format(cmd))
        cmd_list = shlex.split(cmd)
        return subprocess.run(cmd_list, stdout=subprocess.PIPE)

    def test_ERCostHeader(self):
        '''
        Scenario
        1. make urllist
        2. gen testcase
        3. check ER cost
        '''
        # 1. make urllist
        with open(self.URLLIST, 'w') as f:
            f.write('https://fract.akamaized.net/')
        self.assertTrue( os.path.isfile(self.URLLIST))

        # 2. gen testcase
        self.do_cmd( 'python3 {} testgen -i {} -o {} -s fract.akamaized.net -d fract.akamaized-staging.net'.format(fraui_path, self.URLLIST, self.TESTCASE))
        self.assertTrue( os.path.isfile(self.TESTCASE))
        with open( self.TESTCASE ) as f:
            testcase=json.load(f)
            self.assertTrue( testcase[0]['Request']['Headers']['X-Akamai-Cloudlet-Cost'] == 'true')

        # 3. run and check ER cost
        self.do_cmd('python3 {} run -i {} -o {} -s {} -d {}'.format(fraui_path, self.TESTCASE, self.RESULT, self.SUMMARY, self.TDIFF))
        self.assertTrue( os.path.isfile(self.RESULT))
        self.assertTrue( os.path.isfile(self.SUMMARY))
        self.assertTrue( os.path.isfile(self.TDIFF))
        with open( self.RESULT ) as f:
            result = json.load(f)
            self.assertTrue('X-Akamai-Tapioca-Cost-ER' in result[0]['Response'])

    def test_redirsum(self):
        '''
        Scenario:
        1. gen testcase from existing urllist file "urllist4redirect.txt"
        2. run
        3. export redirect summary
        '''
        # 1. gen testcase
        self.do_cmd('python3 {} testgen -i {} -o {} -s fract.akamaized.net -d fract.akamaized-staging.net'.format(fraui_path, 'urllist4redirect.txt', self.TESTCASE) )
        self.assertTrue( os.path.isfile(self.TESTCASE))
        
        # 2. run
        self.do_cmd('python3 {} run -i {} -o {} -s {} -d {}'.format(fraui_path, self.TESTCASE, self.RESULT, self.SUMMARY, self.TDIFF))
        
        # 3. export redirect summary
        self.do_cmd('python3 {} redirsum -t {} -r {} -o {}'.format(fraui_path, self.TESTCASE, self.RESULT, self.REDIRECT_SUMMARY))
        
        self.assertTrue( os.path.isfile(self.REDIRECT_SUMMARY) )
        
        with open( self.REDIRECT_SUMMARY ) as f:
            redirect_summary = json.load(f)
            self.assertTrue( redirect_summary[0]['Response']['status_code'] in (301, 302, 303, 307) )
            self.assertTrue( 'X-Akamai-Tapioca-Cost-ER' in redirect_summary[0]['Response'] )

    def test_ercost(self):
        '''
        Scenario:
        1. export ercost summary from exisiting result
        '''
        self.do_cmd( 'python3 {} ercost -c 10 -t {} -r {} -o {}'.format(fraui_path, 'testcase4redirect.json', 'result4redirect.json', self.ERCOST_SUMMARY) )

        with open(self.ERCOST_SUMMARY) as f:
            ercost_summary = json.load(f)
            self.assertTrue( len(ercost_summary) == 13)

    def test_ercost2(self):
        '''
        Scenario:
        1. export ercost summary from exisiting result with default cost = 100000000
        '''
        self.do_cmd( 'python3 {} ercost -t {} -r {} -o {}'.format(fraui_path, 'testcase4redirect.json', 'result4redirect.json', self.ERCOST_SUMMARY) )

        with open(self.ERCOST_SUMMARY) as f:
            ercost_summary = json.load(f)
            self.assertTrue( len(ercost_summary) == 3)

    # 2018/08/21 ignore_case_support
    def test_IgnoreCase_not_ignored(self):
        '''
        Scenario
        1. make urllist
        2. gen testcase
        3. check ignorecase
        '''
        # 1. make urllist
        with open(self.URLLIST, 'w') as f:
            f.write('https://fract.akamaized.net/ignore_case/foobar.html')
        self.assertTrue(os.path.isfile(self.URLLIST))

        # 2. gen testcase
        self.do_cmd( 'python3 {} testgen -i {} -o {} -s fract.akamaized.net -d fract.akamaized-staging.net'.format(fraui_path, self.URLLIST, self.TESTCASE))
        self.assertTrue( os.path.isfile(self.TESTCASE))
        with open( self.TESTCASE ) as f:
            testcase=json.load(f)
            self.assertTrue( testcase[0]['TestCase']['X-Cache-Key'][0]['option']['ignore_case'] == False)

        # 3. run and check ER cost
        self.do_cmd('python3 {} run -i {} -o {} -s {} -d {}'.format(fraui_path, self.TESTCASE, self.RESULT, self.SUMMARY, self.TDIFF))
        self.assertTrue( os.path.isfile(self.RESULT))
        self.assertTrue( os.path.isfile(self.SUMMARY))
        self.assertTrue( os.path.isfile(self.TDIFF))
        with open( self.RESULT ) as f:
            result = json.load(f)
            self.assertTrue(result[0]['Passed'] == False)

    def test_IgnoreCase_ignored(self):
        '''
        Scenario
        1. make urllist
        2. gen testcase
        3. check ignore case
        '''
        # 1. make urllist
        with open(self.URLLIST, 'w') as f:
            f.write('https://fract.akamaized.net/ignore_case/foobar.html')
        self.assertTrue( os.path.isfile(self.URLLIST))

        # 2. gen testcase
        self.do_cmd( 'python3 {} testgen -i {} -o {} -s fract.akamaized.net -d fract.akamaized-staging.net -I'.format(fraui_path, self.URLLIST, self.TESTCASE))
        self.assertTrue( os.path.isfile(self.TESTCASE))
        with open( self.TESTCASE ) as f:
            testcase=json.load(f)
            self.assertTrue( testcase[0]['TestCase']['X-Cache-Key'][0]['option']['ignore_case'] == True)

        # 3. run and check ER cost
        self.do_cmd('python3 {} run -i {} -o {} -s {} -d {}'.format(fraui_path, self.TESTCASE, self.RESULT, self.SUMMARY, self.TDIFF))
        self.assertTrue( os.path.isfile(self.RESULT))
        self.assertTrue( os.path.isfile(self.SUMMARY))
        self.assertTrue( os.path.isfile(self.TDIFF))
        with open( self.RESULT ) as f:
            result = json.load(f)
            self.assertTrue(result[0]['Passed'] == True)

if __name__ == '__main__':
    print('Version 0.1')
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
