'''
Created on Nov 10, 2009

@author: Armin Primadi
'''

import sgmllib
import os

from model.manga import Manga

"""Parse gotlurk.net manga list page"""
class HTMLParser(sgmllib.SGMLParser):
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)

        self.data = []

        # temp
        self.row = {}

        self.inside_tr = False
        self.inside_td = False

        self.column = 0

    def start_tr(self, attributes):
        self.inside_tr = True

    def end_tr(self):
        self.inside_tr = False

        try:
            self.row['pack_id'] = int(self.row['pack_id'])
            self.row['title']
            self.row['size']
        except (ValueError, KeyError):
            pass # bad row
        else:
            manga = Manga("", **self.row) 
            self.data.append(manga)

        self.row = {}
        self.column = 0

    def start_td(self, attributes):
        self.inside_td = True

    def end_td(self):
        self.inside_td = False
        self.column += 1

    def handle_data(self, data):
        if self.inside_tr and self.inside_td:
            if self.column == 1:
                self.row['pack_id'] = data
            elif self.column == 3:
                self.row['size'] = data
            elif self.column == 4:
                self.row['title'] = os.path.splitext(data)[0]
        