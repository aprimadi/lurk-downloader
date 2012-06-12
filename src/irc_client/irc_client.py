'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import socket
import os

from third_party import irclib
from third_party.irclib import SimpleIRCClient
from model.manga import Manga
from downloader import Downloader

"""Handles all network connection"""
class IRCClient(SimpleIRCClient):

    servername = 'irc.irchighway.net'
    port = 6667
    channel = '#lurk'
    manga_dir = 'manga'

    def __init__(self):
        SimpleIRCClient.__init__(self)

        self.connection_status = 'not_connected'
        self.downloader = Downloader(self.connection)

    """Connecting to the manga server"""
    def connect(self, nickname, password):
        if self.connection_status == 'connected':
            return
        
        try:
            server = socket.gethostbyname(self.servername)
        except socket.error:
            print 'connect failed: make sure that you are connected to the internet and try again'

        try:
            self.connection.connect(server, self.port, nickname, password)
            self.connection.user(nickname, nickname)
            print 'connecting'
        except:
            print 'connect failed: make sure that you are connected to the internet and try again'

    """Start the client"""
    def start(self):
        while 1:
            self.downloader.check()
    
            self.ircobj.process_once(0.2)

    """Request the client to download a manga"""
    def download(self, manga, manga_directory = 'manga'):
        self.downloader.download(manga)

    """Get connection_status"""
    def connection_status(self):
        return self.connection_status

    def on_welcome(self, connection, event):
        self.connection.join(self.channel)
        self.connection_status = 'connected'
        self.downloader.start()
        print 'connected'

    def on_ctcp(self, connection, event):
        try:
            # print event.arguments()
            args = event.arguments()[1].split()
        except IndexError:
            return

        if args[0] != "SEND":
            return
        
        # DCC SEND requested
        
        # check file extension
        file_name = os.path.basename(args[1])
        file_ext = os.path.splitext(file_name)[1]
        file_size = int(args[4])
        if file_ext not in ['.zip', '.rar']:
            return
        file_name = os.path.join(self.manga_dir, file_name)

        # initiate DCC connection
        peeraddress = irclib.ip_numstr_to_quad(args[2])
        peerport = int(args[3])
        self.dcc = self.dcc_connect(peeraddress, peerport, 'raw')
        
        self.downloader.initiate_download(file_name, file_size, self.dcc)

    def on_dccmsg(self, connection, event):
        data = event.arguments()[0]
        self.downloader.receive_data( data )

    def on_dcc_disconnect(self, connection, event):
        self.downloader.finish_download()
        self.downloader.download_next()

    def on_disconnect(self, connection, event):
        self.connection_status = 'disconnected'
        self.downloader.stop()
    
if __name__ == '__main__':
    downloader = IRCClient()
    downloader.connect('zero_cool', 'password')
    downloader.download(Manga('Neverwhere', 2881, 'Whatever', 59))
    downloader.start()
