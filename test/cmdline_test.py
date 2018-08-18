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
    def test_ERCostHeader(self):
        '''
        Scenario
        1. make urllist
        2. gen testcase
        3. check ER cost
        4. rm files
        '''
        URLLIST='urllist.txt.test'
        TESTCASE='testcase.json.test'
        RESULT='result.json.test'
        SUMMARY='summary.txt.test'
        TDIFF='testdiff.yaml.test'
        
        cmd='rm *.test'
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        
        # 1. make urllist
        with open(URLLIST, 'w') as f:
            f.write('https://fract.akamaized.net/')
        self.assertTrue( os.path.isfile(URLLIST))

        # 2. gen testcase
        cmdraw='python3 {} testgen -i {} -o {} -s fract.akamaized.net -d fract.akamaized.net'.format(fraui_path, URLLIST, TESTCASE)
        cmd=shlex.split(cmdraw)
        subprocess.run(cmd, stdout=subprocess.PIPE)
        self.assertTrue( os.path.isfile(TESTCASE))
        with open( TESTCASE ) as f:
            testcase=json.load(f)
            self.assertTrue( testcase[0]['Request']['Headers']['X-Akamai-Cloudlet-Cost'] == 'true')

        # 3. run and check ER cost
        cmdraw='python3 {} run -i {} -o {} -s {} -d {}'.format(fraui_path, TESTCASE, RESULT, SUMMARY, TDIFF)
        cmd=shlex.split(cmdraw)
        subprocess.run(cmd, stdout=subprocess.PIPE)
        self.assertTrue( os.path.isfile(RESULT))
        self.assertTrue( os.path.isfile(SUMMARY))
        self.assertTrue( os.path.isfile(TDIFF))
        with open( RESULT ) as f:
            result = json.load(f)
            self.assertTrue('X-Akamai-Tapioca-Cost-ER' in result[0]['Response'])

        # 4. remove files
        cmd='rm *.test'
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)



if __name__ == '__main__':
    print('Version 0.1')
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    print('All Process End')
