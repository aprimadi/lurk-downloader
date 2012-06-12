'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import unittest
import threading

from tokenizer import Tokenizer

class SearchEngine(object):
	"""
	Constructor
	
	@param data - a list of objects
	@param index - a dictionary which maps term to objects
					in data
	@param tokenizer - a Tokenizer instance which specifies
						how a user query is going to be tokenized
						for evaluation purpose
	"""
	def __init__(self, data, index, tokenizer):
		self.index = index
		self.data = data
		self.tokenizer = tokenizer
		self.lock = threading.Lock()
	
	"""
	Evaluates user supplied query and return data
	based on the index and data file
	
	@param query - a raw string which specifies a user query
	@return results - list of objects that conforms to the query
	"""
	def search(self, query=''):
		terms = self.tokenizer.tokenize(query)
		
		self.lock.acquire()
		
		if (len(terms)==0):
			result = self.data
			self.lock.release()
			return result

		result_set = self.index[terms[0]].copy()
		for i in range(1, len(terms)):
			try:
				set2 = self.index[terms[i]]
			except KeyError:
				set2 = set()
			result_set.intersection_update(set2)

		result = []
		for record_id in result_set:
			result.append( self.data[record_id] )
			
		self.lock.release()

		return result
	
	"""
	Set data and index
	
	@param data - a list of objects
	@param index - a dictionary which maps term to objects
					in data
	"""
	def setDataAndIndex(self, data, index):
		self.lock.acquire()
		
		self.index = index
		self.data = data
		
		self.lock.release()
	
class TestSearchEngine(unittest.TestCase):
	def test_search1(self):
		data = range(0, 10)
		index = { 'one' : set([0, 1]),
				  'piece' : set([0, 5]),
				  'futari' : set([4, 9]),
				  'ecchi' : set([4, 9]) }
		
		tokenizer = Tokenizer()
		searchEngine = SearchEngine(data, index, tokenizer)
		
		result = searchEngine.search('one piece')
		self.assertTrue( len(result) == 1 )
		
		result = searchEngine.search('futari echi')
		self.assertTrue(len(result) == 0)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchEngine)
	unittest.TextTestRunner(verbosity=2).run(suite)