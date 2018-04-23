import unittest, json, logging

from frase import Htmlpsr
class test_Htmlpsr(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_handle_starttag(self):
        hp=Htmlpsr()
        html='''<!DOCTYPE html><html lang="en"><head> <title>Bootstrap Example</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> <script src="maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> <script src="//example.com/foo.js"></script></head><body><a target="_top" href="bootstrap_filters.asp">BS Filters</a><div class="jumbotron text-center"> <h1>My First Bootstrap Page</h1> <p>Resize this responsive page to see the effect!</p><img src="bs_themes.jpg" style="width:98%;margin:20px 0" alt="Theme Company"></div></body></html>'''
        hp.start(html)
        self.assertTrue( hp.anchors[0] == 'bootstrap_filters.asp')
        self.assertTrue( len(hp.embs) == 5)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
