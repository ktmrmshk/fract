import unittest, logging, argparse, os, datetime, subprocess
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

if __name__ == '__main__':
    print('Version 0.1')
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    print('All Process End')
