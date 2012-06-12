'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import threading

import unittest

"""
Thread safe queue
"""
class Queue(object):
    """Constructor"""
    def __init__(self):
        self.lock = threading.Lock()
        self.container = []
  
    """
    Push an item to the back of the queue
    """
    def push(self, item):
        self.lock.acquire()
        self.container.append(item)
        self.lock.release()

    """
    Pop an item from the queue
    
    @return an item on the front of the queue or None if queue is empty
    """
    def pop(self):
        if self.isEmpty():
            return None

        self.lock.acquire()
        
        item = self.container[0]
        del self.container[0]
    
        self.lock.release()
        
        return item

    """
    Check if the queue is empty
    """
    def isEmpty(self):
        return (len(self.container) == 0)

    """
    Clear all item from the queue
    """
    def clear(self):
        self.lock.acquire()
        self.container = []
        self.lock.release()

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_push(self):
        self.queue.push(1)
        item = self.queue.pop()
        self.assertEqual(item, 1)
        self.assertEqual(True, self.queue.isEmpty())
        
    def test_pop(self):
        ret = self.queue.pop()
        self.assertEqual(None, ret)

    def test_order(self):
        order1 = range(0, 10)
        for i in range(0, 10):
            self.queue.push(i)

        order2 = []
        while not self.queue.isEmpty():
            order2.append(self.queue.pop())
    
        self.assertEqual(order1, order2)

    def test_isEmpty(self):
        self.assertTrue(self.queue.isEmpty())
        self.queue.push(1)
        self.assertFalse(self.queue.isEmpty())

    def test_clear(self):
        self.assertTrue(self.queue.isEmpty())
        for i in range(0, 10):
            self.queue.push(i)
        self.assertFalse(self.queue.isEmpty())
        self.queue.clear()
        self.assertTrue(self.queue.isEmpty())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQueue)
    unittest.TextTestRunner(verbosity=2).run(suite)