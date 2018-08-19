import unittest, logging, argparse, os, datetime, subprocess, shlex, json
from pathlib import Path

basePath = os.path.abspath(os.path.dirname(__file__))
envpath = './fratest-output'
totalLogs = ''
fraui_path = os.path.join(Path(basePath).parent, 'src/fraui.py')

class testFractCommnand(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fraui_path = fraui_path
        self.command = ''
        if (os.path.isfile('./urllist.txt')):
            os.remove('./urllist.txt')

    @classmethod
    def tearDownClass(self):
        pass

    def test_HelpInformation(self):
        self.command = ['python3', fraui_path]
        result = subprocess.run(self.command, stdout=subprocess.PIPE)
        stdout_org = result.stdout.decode('utf-8')
        logging.info('Testing Help Information')
        self.assertIn('usage: fract [-h] [-v]', stdout_org)

    def test_GetURLc(self):
        self.command = ['python3', fraui_path, 'geturlc', '-e', 'https://www.uniqlo.com/', '-d', '1', '-o', 'urllist.txt', '-D', 'www.uniqlo.com']
        subprocess.run(self.command, stdout=subprocess.PIPE)
        self.assertTrue(os.path.isfile('./urllist.txt'))

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



if __name__ == '__main__':
    print('Version 0.1')
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    print('All Process End')
