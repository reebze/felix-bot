# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 reebze, Be3y4uu-K0T

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__title__     = 'felix-bot/database'
__author__    = ['reebze','Be3y4uu-K0T']
__copyright__ = 'Copyright 2020 (c) 2020 Be3y4uu_K0T'
__license__   = 'MIT'
__version__   = '0.0.2'
__status__    = 'Development'

#======================================
from discord import logging
import sqlite3
db = sqlite3.connect(r'src\exts\server.db')

logging.basicConfig(filename = r"src\exts\felix.log", 
                    #stream  = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s - : %(name)s : %(message)s', 
                    datefmt  = '%d/%m/%Y#%H:%M:%S')
log = logging.getLogger(__name__)

class sql():
    
    def __init__(self):
        pass
        
    def commit(self):
        global db
        db.commit()
        log.info('DataBase Saved')
        
    def __enter__(self):
        global db
        self.sql_cursor = db.cursor()
        log.info('DataBase.Cursor created') 
        return self.sql_cursor
        
    def __exit__(self, type, value, traceback):
        global db
        self.sql_cursor.close()
        log.info('Close DataBase.Cursor')
        db.commit()
        log.info('DataBase Saved')
