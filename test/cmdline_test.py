import unittest, logging, argparse, os, datetime, subprocess
from pathlib import Path

basePath = os.path.abspath(os.path.dirname(__file__))
envpathout = './cmdline_test_output'
envpathin = './cmdline_test_input'

totalLogs = ''
fraui_path = os.path.join(Path(basePath).parent, './src/fraui.py')
topurllistPath = os.path.join(envpathin, 'fract.akamaized.net_urls.csv')
urllistPath = os.path.join(envpathout, 'urllist.txt')

if not os.path.isdir(envpathout):
    os.mkdir(envpathout)
if not os.path.isdir(envpathin):
    os.mkdir(envpathin)

class testFractCommnand(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fraui_path = fraui_path
        self.command = ''

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        if (os.path.isfile(urllistPath)):
            os.remove(urllistPath)

    def test_HelpInformation(self):
        logging.info('Testing: Help Information Output')
        self.command = ['python3', fraui_path]
        result = subprocess.run(self.command, stdout=subprocess.PIPE)
        stdout_org = result.stdout.decode('utf-8')
        self.assertIn('usage: fract [-h] [-v]', stdout_org)

    def test_GetURLc(self):
        logging.info('Testing: URL generation')
        self.command = ['python3', fraui_path, 'geturlc', '-e', 'https://fract.akamaized.net/', '-d', '1', '-o', urllistPath, '-D', 'fract.akamaized.net']
        subprocess.run(self.command, stdout=subprocess.PIPE)
        self.assertTrue(os.path.isfile(urllistPath))
        if os.path.isfile(urllistPath):
            with open(urllistPath, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('https://fract.akamaized.net/css/main.css') > 0)

    def test_GetURLcFromCSV(self):
        logging.info('Testing: URL generation by Akamai top url')
        self.command = ['python3', fraui_path, 'geturlakm', '-i', topurllistPath, '-D', 'fract.akamaized.net', '-p', 'https', '-o', urllistPath]
        subprocess.run(self.command, stdout=subprocess.PIPE)
        self.assertTrue(os.path.isfile(urllistPath))
        if os.path.isfile(urllistPath):
            with open(urllistPath, mode='r') as rf:
                contents = rf.read()
                self.assertTrue(contents.index('https://fract.akamaized.net/css/main.css') > 0)

    def test_Maketestcases(self):
        pass

if __name__ == '__main__':
    print('Version 0.1')
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
