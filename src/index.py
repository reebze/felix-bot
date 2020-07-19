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

__title__     = 'felix-bot'
__author__    = ['reebze','Be3y4uu-K0T']
__copyright__ = 'Copyright 2020 (c) 2020 Be3y4uu_K0T'
__license__   = 'MIT'
__version__   = '0.2.6'
__status__    = 'Development'

#======================================
import discord as ds
import asyncio
import sqlite3
import sys

from discord.ext import commands, tasks
from datetime import datetime
from discord import logging

if len(sys.argv) <= 1:
    raise ValueError('Token is empty') from None

logging.basicConfig(filename = "felix.log", 
                    #stream  = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s] - : %(name)s : %(message)s', 
                    datefmt  = '%d/%m/%Y#%H:%M:%S')
                    
bot = commands.Bot(command_prefix = "f!")
log = logging.getLogger(__name__)
cogs = ['events',
        'commands',
        'music',
        'games',]
          
if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(f'cogs.{cog}')
    bot.felix_server  = 728988042987307091
    bot.felix_channel = 728991407662039140
    log.info('bot $ Felix starting')
    print('bot $ Felix starting')
    bot.run(sys.argv[1], bot = True, reconnect = True)
