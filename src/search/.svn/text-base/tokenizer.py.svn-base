'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import re
import unittest

class Tokenizer(object):
    """Constructor"""
    def __init__(self):
        pass
        
    """
    Tokenize a string into tokens.
    
    @param s - a string
    @return tokens - list of tokens
    """
    def tokenize(self, s):
        s = s.lower()
        tokens = re.split('\W|_+', s)
        tokens = filter(lambda x: x != '', tokens)
        return tokens
    
class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        terms = Tokenizer().tokenize('One_Piece_v45[zombie]')
        answer = ['one', 'piece', 'v45', 'zombie']
        self.assertEqual(terms, answer)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTokenizer)
    unittest.TextTestRunner(verbosity=2).run(suite)