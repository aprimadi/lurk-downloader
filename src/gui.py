#!/usr/bin/python

from Tkinter import *
import thread
import pickle
import os

from miner.miner import Miner
from search.indexer import Indexer
from search.search_engine import SearchEngine
from search.tokenizer import Tokenizer
from irc_client.irc_client import IRCClient

"""Gui class"""
class Gui(object):
    """
    Initialize the search engine and irc client.
    Also starts a background thread which updates manga
    lists. 
    """
    def __init__(self):
        tokenizer = Tokenizer()
        
        if os.path.exists('manga.dat'): 
            file = open('manga.dat', 'r')
            data = pickle.load(file)
            file.close()
        else:
            data = Miner().mine()
            file = open('manga.dat', 'wb')
            pickle.dump(data, file)
            file.close()

        if os.path.exists('manga.idx'):
            file = open('manga.idx', 'r')
            index = pickle.load(file)
            file.close()
        else:
            indexer = Indexer(tokenizer)
            index = indexer.buildIndex(data)
            file = open('manga.idx', 'wb')
            pickle.dump(index, file)
            file.close()
        
        self.searchEngine = SearchEngine(data, index, tokenizer)
        self.irc_client = IRCClient()
        
        thread.start_new_thread(self.irc_client.start, ())
        thread.start_new_thread(self.refreshList, ())

    """Define gui layouts and start Tk mainloop()"""
    def run(self):
        root = Tk()
        root.geometry("800x600")
    
        frame = Frame(root, width=800, height=600)
        frame.master.title('Lurk Manga Downloader')
        frame.pack()
    
        #######################################################################
    
        topFrame = Frame(frame)
        topFrame.pack(side=TOP, fill=X)
    
        self.searchLabel = Label(topFrame, text="Search: ")
        self.searchLabel.pack(side=LEFT)
    
        self.searchEntry = Entry(topFrame)
        self.searchEntry.pack(side=LEFT)
    
        self.searchButton = Button(topFrame, text="search")
        self.searchButton.pack(side=LEFT)
    
        self.searchEntry.bind("<Return>", self.searchCallback)
        self.searchButton.bind("<Button-1>", self.searchCallback)
    
        #######################################################################
    
        bottomFrame = Frame(frame)
        bottomFrame.pack(side=TOP)
    
        #######################################################################
    
        bottomRightFrame = Frame(bottomFrame)
        bottomRightFrame.pack(side=RIGHT, fill=Y)
    
        self.nickLabel = Label(bottomRightFrame, text="Nickname: ")
        self.nickLabel.pack(side=TOP)
    
        self.nickEntry = Entry(bottomRightFrame)
        self.nickEntry.pack(side=TOP)
    
        self.passLabel = Label(bottomRightFrame, text="Password: ")
        self.passLabel.pack(side=TOP)
    
        self.passEntry = Entry(bottomRightFrame, show='*')
        self.passEntry.pack(side=TOP)
    
        self.connectButton = Button(bottomRightFrame, text="Connect")
        self.connectButton.pack(side=TOP)
        self.connectButton.bind("<Button-1>", self.connectCallback)
    
        self.downloadButton = Button(bottomRightFrame, text="Download")
        self.downloadButton.pack(side=TOP)
        self.downloadButton.bind("<Button-1>", self.downloadCallback)
    
        #######################################################################
    
        self.scrollbar = Scrollbar(bottomFrame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
    
        self.listbox = Listbox(bottomFrame, yscrollcommand=self.scrollbar.set, 
                               width=800, height=600, selectmode=EXTENDED)
        self.mangaList = self.searchEngine.search()
        for manga in self.mangaList:
            self.listbox.insert(END, manga.title)
        self.listbox.pack(side=LEFT, fill=BOTH)
    
        self.scrollbar.config(command=self.listbox.yview)
        
        root.mainloop()

    """search callback"""
    def searchCallback(self, event):
        filterText = self.searchEntry.get()
        self.listbox.delete(0, END)
        
        self.mangaList = self.searchEngine.search(filterText)
        for manga in self.mangaList:
            self.listbox.insert(END, manga.title)

    """connect callback"""
    def connectCallback(self, event):
        nickname = self.nickEntry.get()
        password = self.passEntry.get()
    
        self.irc_client.connect(nickname, password)

    """download callback"""
    def downloadCallback(self, event):
        selection = self.listbox.curselection()

        for indexString in selection:
            index = int(indexString)
            self.irc_client.download(self.mangaList[index])
    
    """mine data from gotlurk and refresh manga list"""
    def refreshList(self):
        data= Miner().mine()
        
        tokenizer = Tokenizer()
        indexer = Indexer(tokenizer)
        index = indexer.buildIndex(data)
        
        # save data and index
        file = open('manga.dat', 'wb')
        pickle.dump(data, file)
        file.close()
        
        file = open('manga.idx', 'wb')
        pickle.dump(index, file)
        file.close()
        
        self.searchEngine.setDataAndIndex(data, index)

if __name__ == '__main__':
    gui = Gui()
    gui.run()
