'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import unittest

from tokenizer import Tokenizer
from model.manga import Manga

class Indexer(object):
    """Constructor"""
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        
    """
    Build an index given a list of object to be indexed.
    The index is built based on the string representation
    of the object. 
    
    @param data - list of objects. Each object has to 
                    implement __str__() method
    @param tokenizer - a string tokenizer object
    @return index - a dictionary which maps term to the index
                    where the term occurs in the input data
    """
    def buildIndex(self, data):
        index = {}
        for data_id, data in enumerate(data):
            terms = self.tokenizer.tokenize(data.__str__())
            for term in terms:
                if not term in index.keys():
                    index[term] = set()
                index[term].add(data_id)
        return index

class TestIndexer(unittest.TestCase):
    def test_unit_buildIndex(self):
        data = [ Manga('Mirrors', 1, 'One_Piece_v45', 45),
                 Manga('Mirrors', 2, 'One_Piece_v44', 32) ]
        answer = { 'one' : set([0, 1]), 
                   'piece' : set([0, 1]),
                   'v44': set([1]),
                   'v45': set([0]) }
        
        indexer = Indexer(Tokenizer())
        index = indexer.buildIndex(data)       
        self.assertEqual(index, answer)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndexer)
    unittest.TextTestRunner(verbosity=2).run(suite)