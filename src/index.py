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
__version__   = '0.2.7'
__status__    = 'Development'

#======================================
import discord as ds
import asyncio
import sys

from discord.ext import commands, tasks
from datetime import datetime
from discord import logging

if len(sys.argv) <= 1:
    raise ValueError('Token is empty') from None

logging.basicConfig(filename = r"src\exts\felix.log", 
                    #stream  = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s - : %(name)s : %(message)s', 
                    datefmt  = '%d/%m/%Y#%H:%M:%S')
log = logging.getLogger(__name__)
                 
bot = commands.Bot(command_prefix = "f!")
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
'''
#======================================
from discord.ext import commands, tasks
from urllib.request import urlopen
from discord import logging
import discord as ds
import sqlite3
import sys

if len(sys.argv) == 1:
    raise ValueError('System arguments is empty') from None

logging.basicConfig(filename="felix.log", format='{%(asctime)s} [%(levelname)s] | %(message)s', datefmt='%Y-%m-%d|%H:%M:%S')
bot    = commands.Bot(command_prefix = "f!")
con    = sqlite3.connect('server.db')
sql    = con.cursor()

@bot.event
async def on_ready():
    """ Felix is ready. """
    global server
    server = bot.get_guild(728988042987307091)
    await bot.change_presence(status   = ds.Status.online,
                              activity = ds.Game(name = "Development in GitHub"),
                              url      = "https://github.com/reebze/felix-bot")
    logging.info('bot $ Felix runed')

@tasks.loop(hours=24)
async def reload():
    con.commit()
    data = urlopen("https://raw.githubusercontent.com/reebze/felix-bot/master/.version")
    for line in data:
        latest = line.decode().rstrip("\n").rstrip("\r")
        break
    if latest > __version__:
        bot.remove_cog('Core')
        data = urlopen("https://raw.githubusercontent.com/reebze/felix-bot/master/core.code")
        
        
    
@bot.event
async def on_connect():
    logging.info('bot $ On connected to discord')
    print('bot $ On connected to discord')

async def is_felix_guild(ctx):
    return ctx.guild == server
   
bot.add_check(is_felix_guild)
with open('core.code',encoding = 'utf-8') as corelib:
    exec(corelib.read()[1:],globals(),locals())
bot.run(sys.argv[1])


print(Core)


@tasks.loop(hours=24)
async def updates():
    data = urlopen("https://raw.githubusercontent.com/reebze/felix-bot/master/.version") #пока не может отправлять запрос, потому что репозиторий закрыт
    for line in data:
        new_ver = line.decode()
        break
    new_ver.rstrip("\n").rstrip("\r")
    if new_ver > __version__:
        pass #загрузка новой версии с github
        
@bot.command()
async def card(ctx, member: ds.Member = None):
    if member == None:
        member = ctx.author

    embed = ds.Embed(colour = ds.Color.blue(),title = 'ЛИЧНАЯ КАРТОЧКА',description = member.top_role.mention)
    embed.set_author(name = member.name,   icon_url = member.avatar_url)
    embed.set_footer(text = bot.user.name, icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url = member.avatar_url)

    for data in sql.execute("SELECT data FROM users WHERE user_id = ?",(member.id,)):
        for args in eval(data[0],{'__builtins__':{}}):
            embed.add_field(**args)
        break
    await ctx.send(embed = embed)
'''
