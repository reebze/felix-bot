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

__title__     = 'felix-bot/music'
__author__    = ['reebze','Be3y4uu-K0T']
__copyright__ = 'Copyright 2020 (c) 2020 Be3y4uu_K0T'
__license__   = 'MIT'
__version__   = '0.0.3'
__status__    = 'Development'

#======================================
from discord.ext import commands
from datetime import datetime
from discord import logging
import exts.database as db
import discord as ds
import asyncio
import youtube_dl

logging.basicConfig(filename = r"src\felix.log", 
                    #stream  = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s - : %(name)s : %(message)s', 
                    datefmt  = '%d/%m/%Y#%H:%M:%S')
log = logging.getLogger(__name__)

class MusicCog(commands.Cog, name = 'Music'):

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
       
    async def __del_message(self, ctx, info_message):
        await info_message.add_reaction('🗑️')

        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) == '🗑️' and user == ctx.message.author
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=10.0, check = check_reaction)
        except asyncio.TimeoutError:
            await info_message.remove_reaction('🗑️', ctx.bot.user)
            return False
        else:
            try:
                await info_message.delete()
            except ds.NotFound:
                pass
            try:
                await ctx.message.delete()
            except ds.NotFound:
                pass
            return True
       
    @commands.command(name = 'join')
    #@commands.has_role()
    async def __join_to_voice_channel(self, ctx):
        try:
            await ctx.message.author.voice.channel.connect()
        except AttributeError:
            info_embed = ds.Embed(color = ds.Color.red(), description = 'Вы не находитесь в голосовом канале!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        else:
            info_embed = ds.Embed(color = ds.Color.gold(), description = f'Бот подключился к #{ctx.message.author.voice.channel.name}')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)
        
    @commands.command(name = 'leave')
    #@commands.has_role()
    async def __leave_channel(self, ctx):
        try:
            await ctx.voice_client.disconnect()
        except AttributeError:
            info_embed = ds.Embed(color = ds.Color.red(), description = 'Бот не подключен к голосовому каналу!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        else:
            info_embed = ds.Embed(color = ds.Color.gold(), description = f'Бот отключился от #{ctx.message.author.voice.channel.name}')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)

    @commands.command(name = 'play')
    #@commands.has_role()
    async def __play_music(self, ctx):
        ctx.voice_client.play(ds.FFmpegPCMAudio(r".\the_final_station_14_nowhere_town.mp3"), after=lambda e: print('Конец, возможная ошибка:', e))
        info_embed = ds.Embed(color = ds.Color.gold(), description = f'Шарманка запущена!')
        info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
        message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)
        
    @commands.command(name = 'stop')
    #@commands.has_role()
    async def __stop_music(self, ctx):
        try:
            ctx.voice_client.stop()
        except AttributeError:
            info_embed = ds.Embed(color = ds.Color.red(), description = f'Бот не находится в голосовом канале!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        else:
            info_embed = ds.Embed(color = ds.Color.gold(), description = f'Шарманка остановлена!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)
            
    @commands.command(name = 'pause')
    #@commands.has_role()
    async def __pause_music(self, ctx):
        try:
            ctx.voice_client.pause()
        except AttributeError:
            info_embed = ds.Embed(color = ds.Color.red(), description = f'Бот не находится в голосовом канале!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        else:
            info_embed = ds.Embed(color = ds.Color.gold(), description = f'Шарманка приостановлена!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)

    @commands.command(name = 'resume')
    #@commands.has_role()
    async def __resume_music(self, ctx):
        try:
            ctx.voice_client.resume()
        except AttributeError:
            info_embed = ds.Embed(color = ds.Color.red(), description = f'Бот не находится в голосовом канале!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        else:
            info_embed = ds.Embed(color = ds.Color.gold(), description = f'Шарманка продолжает играть!')
            info_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)
            
def setup(bot):
    bot.add_cog(MusicCog(bot))
















