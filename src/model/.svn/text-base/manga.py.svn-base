'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

"""Represents a manga object as it is stored in the IRC server"""
class Manga(object):
    """
    Constructor
    
    The pair <bot, pack_id> is a unique key and is used to uniquely
    identified a manga for download request. 
    
    @param bot - bot name
    @param pack_id - pack number
    @param title - manga title
    @param size - file size
    """
    def __init__(self, bot, pack_id, title, size):
        self.bot = bot
        self.pack_id = pack_id
        self.title = title
        self.size = size
        
    """
    String representation of this object
    
    @return string
    """
    def __str__(self):
        return self.title