'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import os
import time

import unittest

class DownloadItem(object):
    def __init__(self, manga):
        self.manga = manga
        self.received_bytes = 0
        self.total_bytes = None
        self.file = None        # file handler
        self.file_name = None
        # 1 minute expiry time before sending another request
        self.expired_request_time = time.time() + 60
        self.status = 'download_requested'
        
    def initiateDownload(self, file_name, total_bytes):
        self.total_bytes = total_bytes
        self.file_name = file_name
        self.file = open(file_name, 'wb')
        self.status = 'downloading'
    
    def appendData(self, data):
        self.file.write(data)
        self.received_bytes += len(data)
        
    def finishDownload(self):
        if self.status == 'download_requested':
            return
        
        self.status = 'download_finished'
        self.file.close()
        
        if not self.isDownloaded():
            os.remove(self.file_name)
        
    def isDownloaded(self):
        return (self.total_bytes == self.received_bytes)
    
class TestDownloadItem(unittest.TestCase):
    def test_functionality(self):
        from model.manga import Manga
        
        obj = DownloadItem(Manga("Mirrors", 2314, "Title", 10))
        obj.initiateDownload('temp', 10)
        obj.appendData('abcdefghij')
        obj.finishDownload()
        
        self.assertTrue(obj.isDownloaded())
        
        os.remove('temp')
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDownloadItem)
    unittest.TextTestRunner(verbosity=2).run(suite)