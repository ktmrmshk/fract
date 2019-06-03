'''
fract ui classes
'''
from fract import *
from frase import *
from frmq import *
from fractman import *
import argparse
import logging
from datetime import datetime
import os
from version import VERSION
from config import CONFIG

class fractui(object):
    def __init__(self):
        self.prs=argparse.ArgumentParser(prog='fract')
        self.prs.add_argument('-v', '--verbosity', help='verbos display', action='store_true')
        self.prs.add_argument('--version', help='verion info', action='store_true')
        self.prs.set_defaults(func=self.do_usage)
        subprs=self.prs.add_subparsers(help='sub-command help')
        
        ### geturlc - get url by crawler
        subprs_geturlc=subprs.add_parser('geturlc', help='Get URL list using built-in crawler')
        subprs_geturlc.add_argument('-e', '--entrypoint', help='entry point url e.g. https://www.akamai.com/', required=True)
        subprs_geturlc.add_argument('-d', '--depth', help='depth of crawling. default=1', type=int, default=1)
        subprs_geturlc.add_argument('-o', '--output', help='output filename', required=True)
        subprs_geturlc.add_argument('-D', '--domain', help='domain/FQDN to collect. e.g. www.akamai.com www2.akamai.com ...', nargs='+', required=True)
        subprs_geturlc.set_defaults(func=self.do_geturls)


        ### geturlakm - get url by akamai log
        subprs_geturlc=subprs.add_parser('geturlakm', help='Get URL list using Akamai Top Url List CSV files')
        subprs_geturlc.add_argument('-i', '--input', help='akamai top url csv file', nargs='+', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='output filename', required=True)
        subprs_geturlc.add_argument('-D', '--domain', help='domain/FQDN/Digial Property. e.g. www.akamai.com', required=True)
        subprs_geturlc.add_argument('-p', '--protocol', help='protocol: http or https', default='https')
        subprs_geturlc.set_defaults(func=self.do_geturlakm)




        ### testgen - generate test from url list files
        subprs_geturlc=subprs.add_parser('testgen', help="Testcase generator based on current server's behaviors")
        subprs_geturlc.add_argument('-i', '--input', help='input filename containing url list', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='output testcase file - json formatted', required=True)
        subprs_geturlc.add_argument('-s', '--srcghost', help='src ghost/webserver name', required=True)
        subprs_geturlc.add_argument('-d', '--dstghost', help='dest ghost/webserver name', required=True)
        subprs_geturlc.add_argument('-H', '--headers', help='''custom reqest headers to be appended on testcase requests. Specify json format e.g. -H '{"User-Agent":"iPhone", "Referer":"http://abc.com"}'  ''', default='{}')
        subprs_geturlc.add_argument('-I', '--ignore_case', help='ignore case in test', action='store_true')
        subprs_geturlc.add_argument('--strict-redirect-cacheability', help='to check x-check-cacheability when 30x response', action='store_true', dest='strict_redirect_cacheability')
        subprs_geturlc.set_defaults(func=self.do_testgen)
        

        ### run - run test case and output results
        now=datetime.today()
        mid=now.strftime('%Y%m%d%H%M%S%f')
        
        subprs_geturlc=subprs.add_parser('run', help='Run testcases')
        subprs_geturlc.add_argument('-i', '--input', help='filename of test case json', required=True)
        subprs_geturlc.add_argument('-t', '--testid', help='TestId in test case to run', default=None, nargs='+')
        subprs_geturlc.add_argument('-o', '--output', help='filename for full result output', default=self._tname('fret', 'json', mid=mid))
        subprs_geturlc.add_argument('-s', '--summary', help='filename for summary output', default=self._tname('frsummary', 'txt', mid=mid))
        subprs_geturlc.add_argument('-d', '--diff', help='test case generated based on diffs', default=self._tname('frdiff', 'json', mid=mid))
        subprs_geturlc.set_defaults(func=self.do_run)


        ### tmerge - merge testcase files into one testcase file based on TestId
        subprs_geturlc=subprs.add_parser('tmerge', help='Merge multiple testcases into signle file')
        subprs_geturlc.add_argument('-t', '--testcase', help='testcase json files to merge based on TestId. Latter files overwrite former one.', nargs='+', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='filename of test case json after merging', required=True)
        subprs_geturlc.set_defaults(func=self.do_tmerge)


        ### tmerge - merge testcase files into one testcase file based on TestId
        subprs_geturlc=subprs.add_parser('rmerge', help='Merge multiple results into signle form')
        subprs_geturlc.add_argument('-t', '--testcase', help='testcase json files', nargs='+', required=True)
        subprs_geturlc.add_argument('-r', '--result', help='result json files', nargs='+', required=True)
        subprs_geturlc.add_argument('-s', '--summary', help='filename for summary output', default=self._tname('frsummary', 'txt', mid=mid))
        subprs_geturlc.add_argument('-o', '--output', help='filename for full result output', default=self._tname('fret', 'json', mid=mid))
        subprs_geturlc.set_defaults(func=self.do_rmerge)


        ### j2y - json to yaml converter
        subprs_geturlc=subprs.add_parser('j2y', help='Json to yaml converter')
        subprs_geturlc.add_argument('jsonfile', help='Json filename')
        subprs_geturlc.add_argument('yamlfile', help='Yaml filename')
        subprs_geturlc.set_defaults(func=self.do_j2y)
        

        ### y2j - yaml to json converter
        subprs_geturlc=subprs.add_parser('y2j', help='Yaml to json converter')
        subprs_geturlc.add_argument('yamlfile', help='Yaml filename')
        subprs_geturlc.add_argument('jsonfile', help='Json filename')
        subprs_geturlc.set_defaults(func=self.do_y2j)


        ### redirsum - redirect summary 
        subprs_geturlc=subprs.add_parser('redirsum', help='Export redirect request/response summary in JSON form')
        subprs_geturlc.add_argument('-t', '--testcase', help='testcase json file - input', required=True)
        subprs_geturlc.add_argument('-r', '--result', help='result json file - input', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='filename for summary output', required=True)
        subprs_geturlc.set_defaults(func=self.export_redirect_summary)
        

        ### ercost - ercost-check summary
        subprs_geturlc=subprs.add_parser('ercost', help='Export Eege-Redirector-Cost summary in JSON form')
        default_cost=10000000
        subprs_geturlc.add_argument('-c', '--cost', help='cost threashold to Eege-Redirector-Cost (default {})'.format(default_cost),  type=int, default=default_cost)
        subprs_geturlc.add_argument('-t', '--testcase', help='testcase json file - input', required=True)
        subprs_geturlc.add_argument('-r', '--result', help='result json file - input', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='filename for summary output', required=True)
        subprs_geturlc.set_defaults(func=self.export_ercost_summary)

        ### 2019/04/05 testredirectloop start
        subprs_geturlc=subprs.add_parser('testredirectloop', help='Test if redirect happend more than special value')
        subprs_geturlc.add_argument('-i', '--input', help='input filename containing url list', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='filename for full result output', default=self._tname('loopret', 'json', mid=mid))
        subprs_geturlc.add_argument('-s', '--summary', help='filename for summary output', default=self._tname('loopsummary', 'txt', mid=mid))
        subprs_geturlc.add_argument('-d', '--dstghost', help='dest ghost/webserver name. This is optional. If not specified, it requests to web host based on URL in inputfile.', default=None)
        subprs_geturlc.add_argument('-m', '--maximum', help='threshold to trace redirect chain. default=5', type=int, default=5)
        subprs_geturlc.set_defaults(func=self.do_testredirectloop)
        ### 2019/04/05 testredirectloop end


        ### worker
        subprs_geturlc=subprs.add_parser('worker', help='spawn a worker and subscribe task queue')
        #subprs_geturlc.add_argument('-n', '--name', help='worker name', required=True)
        subprs_geturlc.set_defaults(func=self.spawn_worker)


        ### testgen_pls - generate test from url list files
        subprs_geturlc=subprs.add_parser('testgen_pls', help="Testcase generator based on current server's behaviors")
        subprs_geturlc.add_argument('-i', '--input', help='input filename containing url list', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='output testcase file - json formatted', required=True)
        subprs_geturlc.add_argument('-s', '--srcghost', help='src ghost/webserver name', required=True)
        subprs_geturlc.add_argument('-d', '--dstghost', help='dest ghost/webserver name', required=True)
        subprs_geturlc.add_argument('-H', '--headers', help='''custom reqest headers to be appended on testcase requests. Specify json format e.g. -H '{"User-Agent":"iPhone", "Referer":"http://abc.com"}'  ''', default='{}')
        subprs_geturlc.add_argument('-I', '--ignore_case', help='ignore case in test', action='store_true')
        subprs_geturlc.add_argument('--strict-redirect-cacheability', help='to check x-check-cacheability when 30x response', action='store_true', dest='strict_redirect_cacheability')
        subprs_geturlc.set_defaults(func=self.do_testgen_pls)
        



    def _tname(self, prefix, ext, postfix='', mid=None):
        ' if mid is None, returns "prefix2018111210123postfix.ext" '
        if mid is None:
            now=datetime.today()
            mid=now.strftime('%Y%m%d%H%M%S%f')
        return '{}{}{}.{}'.format(prefix, mid, postfix, ext)

    def verbose(self, args):
        if args.verbosity:
            logging.basicConfig(level=logging.DEBUG)

    def do_usage(self, args):
        self.verbose(args)
        logging.debug(args)
        print('Version: {}'.format(VERSION))
        if args.version == False:
            self.prs.print_help()

    def do_geturls(self, args):
        self.verbose(args)
        logging.debug(args)
        
        hc=Htmlcrwlr(args.entrypoint, args.domain, args.depth)
        hc.start()
        hc.save(args.output)

    def do_geturlakm(self, args):
        self.verbose(args)
        logging.debug(args)
        
        fl=FrakmLog()
        fl.gen(args.domain, args.input, '{}://'.format(args.protocol))
        fl.save(args.output)

    def do_testgen(self, args):
        self.verbose(args)
        logging.debug(args)
        headers=json.loads(args.headers)
        ignore_case=args.ignore_case
        strict_redirect_cacheability = args.strict_redirect_cacheability

        fg=FraseGen()
        fg.gen_from_urls(args.input, args.srcghost, args.dstghost, headers=headers, option={'ignore_case':ignore_case}, mode={ 'strict_redirect_cacheability': strict_redirect_cacheability})
        fg.save(args.output)
        
        logging.info('save to {}'.format(args.output))

    def do_run(self, args):
        self.verbose(args)
        logging.debug(args)

        fclient = FractClient(fract_suite_file=args.input)
        fclient.run_suite(args.testid)
        fclient.export_result(args.output)
        summary = fclient.make_summary()
        print(summary)
        with open(args.summary, 'w') as fw:
            fw.write(summary)

        fclient.export_failed_testsuite(args.diff.replace('.json', '.yaml'), 'yaml')
        logging.info('save to {}'.format(args.output))

    def do_tmerge(self, args):
        self.verbose(args)
        logging.debug(args)
        ftm=FractSuiteManager()
        ftm.load_base_suite(args.testcase[0])
        cnt_merged=0
        cnt_added=0
        for t in args.testcase[1:]:
            merged, added = ftm.merge_suite(t)
            cnt_merged+=merged
            cnt_added+=added
        logging.info('{} merged, {} added\n'.format(cnt_merged, cnt_added))
        ftm.save(args.output)

    def do_rmerge(self, args):
        self.verbose(args)
        logging.debug(args)
        
        ftm=FractSuiteManager()
        ftm.load_base_suite(args.testcase[0])
        for t in args.testcase[1:]:
            ftm.merge_suite(t)

        frm=FractSuiteManager()
        frm.load_base_suite(args.result[0])
        for r in args.result[1:]:
            frm.merge_suite(r)

        testsuite=ftm.get_suite()
        resultsuite=frm.get_suite()

        fclient=FractClient(fract_suite_obj=testsuite)
        fclient.load_result(resultsuite)

        summary=fclient.make_summary()
        print(summary)
        with open(args.summary, 'w') as fw:
            fw.write(summary)

        fclient.export_result(args.output)


    def do_j2y(self, args):
        self.verbose(args)
        logging.debug(args)

        jy=JsonYaml()
        jy.j2y(args.jsonfile, args.yamlfile)

    def do_y2j(self, args):
        self.verbose(args)
        logging.debug(args)

        jy=JsonYaml()
        jy.y2j(args.yamlfile, args.jsonfile)

    def export_redirect_summary(self, args):
        self.verbose(args)
        logging.debug(args)
        
        fclient = FractClient(fract_suite_file=args.testcase)
        fclient.load_resultfile(args.result)
        fclient.export_redirect_summary(args.output)

    def export_ercost_summary(self, args):
        self.verbose(args)
        logging.debug(args)
        
        fclient = FractClient(fract_suite_file=args.testcase)
        fclient.load_resultfile(args.result)
        fclient.export_ercost_high(args.output, args.cost)

    ### 2019/04/05 testredirectloop start
    def do_testredirectloop(self, args):
        self.verbose(args)
        logging.debug(args)
        
        rltester = RedirectLoopTester()
        rltester.test_from_urls(args.input, args.dstghost, args.maximum)
        rltester.save(args.output, args.summary, args.maximum)

        logging.info('Result saved to {}'.format(args.output))
        logging.info('Summary saved to {}'.format(args.summary))
    ### 2019/04/05 testredirectloop end

    def spawn_worker(self, args):
        self.verbose(args)
        logging.debug(args)
        
        worker = FractWorker()
        worker.open()
        worker.make_queue(CONFIG['mq']['queuename'])
        worker.addCallback('testgen', Subtask_TestGen.do_task)
        worker.consume(CONFIG['mq']['queuename'])

    def do_testgen_pls(self, args):
        self.verbose(args)
        logging.debug(args)
        headers=json.loads(args.headers)
        ignore_case=args.ignore_case
        strict_redirect_cacheability = args.strict_redirect_cacheability

        now=datetime.today()
        sessionid=now.strftime('%Y%m%d%H%M%S%f')
        tgm=TestGenMan(sessionid)
        tgm.push_urllist_from_file(args.input, 10, args.srcghost, args.dstghost, headers=headers, options={'ignore_case':ignore_case}, mode={ 'strict_redirect_cacheability': strict_redirect_cacheability})

        tgm.save(args.output, 1)

        logging.info('save to {}'.format(args.output))



if __name__ == '__main__':
    try:
        ui=fractui()
        args = ui.prs.parse_args()
        args.func(args)
    except Exception as e:
        logging.error(e)



