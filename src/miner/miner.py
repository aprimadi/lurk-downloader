'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import urllib
import unittest

from html_parser import HTMLParser
from model.manga import Manga

"""Used to mine Manga lists from gotlurk.net"""
class Miner(object):
    """
    Constructor
    
    @param botlist - list of manga bots to be included
    """
    def __init__(self, botlist = ['Mirrors', 'Neverwhere']):
        self.botlist = botlist

    """retrieve raw html"""
    def retrieveHTML(self, bot):
        postData = urllib.urlencode({'srch': '*/%s' % bot})
        f = urllib.urlopen('http://gotlurk.net/?action=dosearch', postData)
        return f.read()

    """mine data"""
    def mine(self):
        data = []
        for bot in self.botlist:
            raw = self.retrieveHTML(bot)
            
            parser = HTMLParser()
            parser.feed(raw)
            parser.close()
            for manga in parser.data:
                manga.bot = bot
            data.extend(parser.data)
        return data
        
class TestMiner(unittest.TestCase):
    def test_mine(self):
        miner = Miner()
        data = miner.mine()
        self.assertTrue(len(data) > 0)
        
        for item in data:
            self.assertTrue(isinstance(item, Manga))
    
    def test_retrieveHTML(self):
        miner = Miner()
        raw_html = miner.retrieveHTML('Mirrors')
        self.assertTrue(len(raw_html) > 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiner)
    unittest.TextTestRunner(verbosity=2).run(suite)