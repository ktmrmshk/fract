'''
fract ui classes
'''
from fract import *
from frase import *
import argparse
import logging
from datetime import datetime


class fractui(object):
    def __init__(self):
        self.prs=argparse.ArgumentParser(prog='fract')
        self.prs.add_argument('-v', '--verbosity', help='verbos display', action='store_true')
        subprs=self.prs.add_subparsers(help='sub-command help')
        
        ### geturlc - get url by crawler
        subprs_geturlc=subprs.add_parser('geturlc')
        subprs_geturlc.add_argument('-e', '--entrypoint', help='entry point url e.g. https://www.akamai.com/', required=True)
        subprs_geturlc.add_argument('-d', '--depth', help='depth of crawling. default=1', type=int, default=1)
        subprs_geturlc.add_argument('-o', '--output', help='output filename', required=True)
        subprs_geturlc.add_argument('-D', '--domain', help='domain/FQDN to collect. e.g. www.akamai.com www2.akamai.com ...', nargs='+', required=True)
        subprs_geturlc.set_defaults(func=self.do_geturls)


        ### geturlakm - get url by akamai log
        subprs_geturlc=subprs.add_parser('geturlakm')
        subprs_geturlc.add_argument('-i', '--input', help='akamai top url csv file', nargs='+', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='output filename', required=True)
        subprs_geturlc.add_argument('-D', '--domain', help='domain/FQDN/Digial Property. e.g. www.akamai.com', required=True)
        subprs_geturlc.add_argument('-p', '--protocol', help='protocol: http or https', default='https')
        subprs_geturlc.set_defaults(func=self.do_geturlakm)




        ### testget - generate test from url list files
        subprs_geturlc=subprs.add_parser('testgen')
        subprs_geturlc.add_argument('-i', '--input', help='input filename containing url list', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='output testcase file - json formatted', required=True)
        subprs_geturlc.add_argument('-s', '--srcghost', help='src ghost/webserver name', required=True)
        subprs_geturlc.add_argument('-d', '--dstghost', help='dest ghost/webserver name', required=True)
        subprs_geturlc.set_defaults(func=self.do_testgen)
        

        ### run - run test case and output results
        now=datetime.today()
        mid=now.strftime('%Y%m%d%H%M%S%f')
        
        subprs_geturlc=subprs.add_parser('run')
        subprs_geturlc.add_argument('-i', '--input', help='filename of test case json', required=True)
        subprs_geturlc.add_argument('-t', '--testid', help='TestId in test case to run', default=None, nargs='+')
        subprs_geturlc.add_argument('-o', '--output', help='filename for full result output', default=self._tname('fret', 'json', mid=mid))
        subprs_geturlc.add_argument('-s', '--summary', help='filename for summary output', default=self._tname('frsummary', 'txt', mid=mid))
        subprs_geturlc.add_argument('-d', '--diff', help='test case generated based on diffs', default=self._tname('frdiff', 'json', mid=mid))
        subprs_geturlc.set_defaults(func=self.do_run)


        ### tmerge - merge testcase files into one testcase file based on TestId
        subprs_geturlc=subprs.add_parser('tmerge')
        subprs_geturlc.add_argument('-t', '--testcase', help='testcase json files to merge based on TestId. Latter files overwrite former one.', nargs='+', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='filename of test case json after merging', required=True)
        subprs_geturlc.set_defaults(func=self.do_tmerge)


        ### tmerge - merge testcase files into one testcase file based on TestId
        subprs_geturlc=subprs.add_parser('rmerge')
        subprs_geturlc.add_argument('-t', '--testcase', help='testcase json files', nargs='+', required=True)
        subprs_geturlc.add_argument('-r', '--result', help='result json files', nargs='+', required=True)
        subprs_geturlc.add_argument('-s', '--summary', help='filename for summary output', default=self._tname('frsummary', 'txt', mid=mid))
        subprs_geturlc.add_argument('-o', '--output', help='filename for full result output', default=self._tname('fret', 'json', mid=mid))
        subprs_geturlc.set_defaults(func=self.do_rmerge)


        ### j2y - json to yaml converter
        subprs_geturlc=subprs.add_parser('j2y')
        subprs_geturlc.add_argument('jsonfile', help='Json filename')
        subprs_geturlc.add_argument('yamlfile', help='Yaml filename')
        subprs_geturlc.set_defaults(func=self.do_j2y)
        

        ### y2j - yaml to json converter
        subprs_geturlc=subprs.add_parser('y2j')
        subprs_geturlc.add_argument('yamlfile', help='Yaml filename')
        subprs_geturlc.add_argument('jsonfile', help='Json filename')
        subprs_geturlc.set_defaults(func=self.do_y2j)



    def _tname(self, prefix, ext, postfix='', mid=None):
        ' if mid is None, returns "prefix2018111210123postfix.ext" '
        if mid is None:
            now=datetime.today()
            mid=now.strftime('%Y%m%d%H%M%S%f')
        return '{}{}{}.{}'.format(prefix, mid, postfix, ext)

    def verbose(self, args):
        if args.verbosity:
            logging.basicConfig(level=logging.DEBUG)

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
        
        fg=FraseGen()
        fg.gen_from_urls(args.input, args.srcghost, args.dstghost)
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


if __name__ == '__main__':
    ui=fractui()
    args = ui.prs.parse_args()
    args.func(args)




