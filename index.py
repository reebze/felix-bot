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
__version__   = '0.2.3'
__status__    = 'Development'

#======================================
from discord.ext import commands, tasks
from discord import logging
import discord as ds
import traceback
import sqlite3
import sys

#from urllib.request import urlopen
#import git

if len(sys.argv) == 1:
    raise ValueError('System arguments is empty')

logging.basicConfig(filename="felix.log", format='{%(asctime)s} [%(levelname)s] | %(message)s', datefmt='%Y-%m-%d|%H:%M:%S')
bot = commands.Bot(command_prefix = "f!")
con = sqlite3.connect('server.db')
sql = con.cursor()

@bot.event
async def on_ready():
    global server
    server = bot.get_guild(728988042987307091)
    logging.debug('Bot started.')
    print("[BOT STARTED]")

@bot.event
async def on_raw_reaction_add(ctx):
    if data := sql.execute("SELECT role_id FROM emojis WHERE msg_id = ? and emoji = ?",(ctx.message_id,ctx.emoji.name)):
        role = ds.utils.get(server.roles, id = data[0][0])
        member = server.get_member(ctx.user_id)
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(ctx):
    if data := sql.execute("SELECT role_id FROM emojis WHERE msg_id = ? and emoji = ?",(ctx.message_id,ctx.emoji.name)):
        role = ds.utils.get(server.roles, id = data[0][0])
        member = server.get_member(ctx.user_id)
        await member.remove_roles(role)
       
@bot.event
async def on_command_error(ctx, error):
    logging.error(error)
    await ctx.send(embed = ds.Embed(colour = ds.Color.red(),
                                    description = 'Вы вызвали ошибку!'))
    
@bot.event
async def on_error(event, *args, **kwargs):
    message = args[0]
    logging.error(traceback.format_exc())
    await bot.send_message(message.channel, 'Вы вызвали ошибку!') 

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

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await server.get_channel(728991407662039140).send(embed = ds.Embed(colour = ds.Color.yellow(),
                                                                       title = 'Сообщения удалены!'))
                                                                       
bot.run(sys.argv[1])

'''
@tasks.loop(hours=24)
async def updates():
    data = urlopen("https://raw.githubusercontent.com/reebze/felix-bot/master/.version") #пока не может отправлять запрос, потому что репозиторий закрыт
    for line in data:
        new_ver = line.decode()
        break
    new_ver.rstrip("\n").rstrip("\r")
    if new_ver > __version__:
        pass #загрузка новой версии с github
'''
