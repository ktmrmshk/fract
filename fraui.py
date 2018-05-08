'''
fract ui classes
'''
from fract import *
from frase import *
import argparse
import logging



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

        ### testget - generate test from url list files
        subprs_geturlc=subprs.add_parser('testgen')
        subprs_geturlc.add_argument('-i', '--input', help='input filename containing url list', required=True)
        subprs_geturlc.add_argument('-o', '--output', help='output testcase file - json formatted', required=True)
        subprs_geturlc.add_argument('-s', '--srcghost', help='src ghost/webserver name', required=True)
        subprs_geturlc.add_argument('-d', '--dstghost', help='dest ghost/webserver name', required=True)
        subprs_geturlc.set_defaults(func=self.do_testgen)
        


    def verbose(self, args):
        if args.verbosity:
            logging.basicConfig(level=logging.DEBUG)

    def do_geturls(self, args):
        self.verbose(args)
        logging.debug(args)
        
        hc=Htmlcrwlr(args.entrypoint, args.domain, args.depth)
        hc.start()
        hc.save(args.output)

    def do_testgen(self, args):
        self.verbose(args)
        logging.debug(args)
        
        fg=FraseGen()
        fg.gen_from_urls(args.input, args.srcghost, args.dstghost)
        fg.save(args.output)
        
        logging.info('save to {}'.format(args.output))






if __name__ == '__main__':
    ui=fractui()
    args = ui.prs.parse_args()
    args.func(args)




