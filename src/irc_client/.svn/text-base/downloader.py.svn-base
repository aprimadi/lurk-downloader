'''
Created on Nov 13, 2009

@author: Armin Primadi
'''

import struct
import time

import unittest

from download_item import DownloadItem
from utils.queue import Queue

class Downloader(object):
    """constructor"""
    def __init__(self, connection):
        self.download_queue = Queue()
        self.current_download = None
        
        self.download_status = 'not_ready'
        self.connection = connection
        self.dcc_connection = None
        
    """start downloader"""
    def start(self):
        self.download_status = 'ready'
        
    """stop downloader"""
    def stop(self):
        self.download_status = 'not_ready'
        
    """is it ready for download?"""
    def is_ready(self):
        return (self.download_status == 'ready')
    
    """add manga to download_queue"""
    def download(self, manga):
        print "Adding %s to download queue" % manga.title
        self.download_queue.push(manga)
        
    """check for download status and determine action to take"""
    def check(self):
        if self.is_ready():
            self.download_next()
        elif ( self.download_status == 'requesting_download' and 
               self.current_download.expired_request_time < time.time() ):
            self.finish_download()
        
    """pop an item from download_queue and request download"""
    def download_next(self):
        assert(self.is_ready())
        
        if self.current_download is not None and not self.current_download.isDownloaded():
            # restart download
            manga = self.current_download.manga
        else:
            manga = self.download_queue.pop()
            if (manga is None):
                return
        
        print "Requesting download of %s" % manga.title
        self.current_download = DownloadItem(manga)
        self.connection.privmsg(manga.bot, "XDCC SEND #%d" % manga.pack_id)
        self.download_status = 'requesting_download'
        
    """initiate a manga download connection"""
    def initiate_download(self, file_name, file_size, dcc_connection):
        print "Downloading %s" % self.current_download.manga.title
        self.download_status = 'downloading'
        self.dcc_connection = dcc_connection
        
        self.current_download.initiateDownload(file_name, file_size)
    
    """receive download data"""
    def receive_data(self, data):
        self.current_download.appendData(data)
        self.dcc_connection.privmsg(struct.pack("!I", self.current_download.received_bytes))
    
    """clean up dcc connection and its state"""
    def finish_download(self):
        if (self.current_download.isDownloaded()):
            print "Finished downloading %s\n" % self.current_download.manga.title
        else:
            print "Failed downloading %s" % self.current_download.manga.title
        self.current_download.finishDownload()
        self.download_status = 'ready'
        self.dcc_connection = None
        
class TestDownloader(unittest.TestCase):
    def test_functionality(self):
        # TODO: write test for Downloader class
        self.assertTrue(1)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDownloader)
    unittest.TextTestRunner(verbosity=2).run(suite)