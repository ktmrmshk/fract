import subprocess, os, logging, time, json
import unittest

class TestFractPlus(unittest.TestCase):
    def setUp(self):
        ### docker build
        cmd='docker build -f docker/Dockerfile -t fract/dev .'
        subprocess.check_call(cmd.split(' '), cwd='../')

        ### mongo and rabbit mq up
        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml up -d mongodb rabbitmq'
        subprocess.check_call(cmd.split(' '))

        # waiting until rabbitmq server is ready
        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml run --rm fract fract wait_mq_ready'
        subprocess.check_call(cmd.split(' '))

        ### worker up
        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml up -d --scale worker=2'
        subprocess.check_call(cmd.split(' '))

    def tearDown(self):
        ### stop mongo and rabbitmq
        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml down'
        subprocess.check_call(cmd.split(' '))

        
    def test_testgen_pls_simple(self):
        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml run --rm -v{}:/this fract fract testgen_pls -i /this/urllist4inactive.txt -o /this/testcase123.json -s fract.akamaized.net -d fract.akamaized.net'.format(os.getcwd())
        subprocess.check_call(cmd.split(' '))

        with open('testcase123.json') as f:
            testcases=json.load(f)
            self.assertTrue( len(testcases) == 3)
            self.assertTrue( 'X-Check-Cacheable' not in testcases[0]['TestCase'] )
            self.assertTrue( testcases[0]['TestCase']['X-Cache-Key'][0]['option']['ignore_case'] == False)

    def test_testgen_pls_options(self):
        cmd='''docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml run --rm -v{}:/this fract fract testgen_pls -i /this/urllist4inactive.txt -o /this/testcase123.json -s fract.akamaized.net -d fract.akamaized.net -H {{"User-Agent":"iPhone","Referer":"http://www.uniqlo.com/"}} --strict-check-cacheability --ignore_case'''.format(os.getcwd())
        subprocess.check_call(cmd.split(' '))

        with open('testcase123.json') as f:
            testcases=json.load(f)
            self.assertTrue( testcases[0]['Request']['Headers']['User-Agent'] == 'iPhone')
            self.assertTrue( testcases[0]['Request']['Headers']['Referer'] == 'http://www.uniqlo.com/')
            self.assertTrue( testcases[0]['Request']['Headers']['X-Akamai-Cloudlet-Cost'] == "true")
            self.assertTrue( testcases[0]['Request']['Headers']['Cookie'] == 'akamai-rum=off')
            
            self.assertTrue( 'X-Check-Cacheable' in testcases[0]['TestCase'] )
            self.assertTrue( testcases[0]['TestCase']['X-Cache-Key'][0]['option']['ignore_case'] == True)

            


    def test_run_pls(self):
        infile='testcasejson4mongodbtest.json'
        outfile='out123.json'
        summary='summary123.json'
        diff='diff123.json'

        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml run --rm -v{}:/this fract fract run_pls -i /this/{} -o /this/{} -s /this/{} -d /this/{}'.format(os.getcwd(), infile, outfile, summary, diff)
        subprocess.check_call(cmd.split(' '))

        with open(outfile) as f:
            testcases=json.load(f)
            self.assertTrue( len(testcases) == 3)

        self.assertTrue( os.path.exists(summary)  )
        #self.assertTrue( os.path.exists(diff)  )

    
    def test_testgen_run_pls(self):
        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml run --rm -v{}:/this fract fract testgen_pls -i /this/{} -o /this/{} -s {} -d {}'.format(os.getcwd(), 'urllist2.txt', 't.json', 'www.uniqlo.com', 'www.uniqlo.com')
        subprocess.check_call(cmd.split(' '))
        
        cmd='docker-compose -p test_fract_pls -f ../docker-compose-dev/docker-compose.yml run --rm -v{}:/this fract fract run_pls -i /this/{}'.format(os.getcwd(), 't.json')
        subprocess.check_call(cmd.split(' '))
        


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
