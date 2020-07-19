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
#======================================
from discord.ext import commands
from datetime import datetime
from discord import logging
import database as db
import discord as ds
import asyncio

logging.basicConfig(filename = "felix.log", 
                    #stream  = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s] - : %(name)s : %(message)s', 
                    datefmt  = '%d/%m/%Y#%H:%M:%S')
log = logging.getLogger(__name__)

class GamesCog(commands.Cog, name = 'Games'):

    def __init__(self, bot):
        self.bot = bot
        
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
        
    @commands.command(name = 'playgame')
    async def __play_in_game(self, ctx):
        
        red    = ':red_square:'
        orange = ':orange_square:'
        yellow = ':yellow_square:'
        green  = ':green_square:'
        blue   = ':blue_square:'
        purple = ':purple_square:'
        brown  = ':brown_square:'
        black  = ':black_large_square:'
        neg    = ':negative_squared_cross_mark:'
        pos    = ':white_check_mark:'
        player = '<:felix_game:734415021425164330>'
        game_field = [ [red,  red,    red,    red,    red,    red,    red,],
                       [red,  player, black,  black,  black,  black,  red,],
                       [red,  black,  black,  black,  black,  black,  red,],
                       [red,  black,  black,  black,  black,  black,  red,],
                       [red,  neg,    black,  black,  black,  black,  red,],
                       [red,  black,  black,  black,  black,  pos,    red,],
                       [red,  red,    red,    red,    red,    red,    red,],
               ]
        game_embed = ds.Embed(color = ds.Color.green(), title = 'Уровень # 1!', description = '\n'.join([''.join(line) for line in game_field]))
        game_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
        game_message = await ctx.send(embed = game_embed)
        asyncio.gather(*[game_message.add_reaction(emoji) for emoji in '⬅⬆➡⬇🔄'])
        def check_reaction(reaction, user):
            return user == ctx.message.author and reaction.message.id == game_message.id and reaction.emoji.name in '⬅⬆➡⬇🔄'
            
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout = 25.0, check = check_reaction)
        except asyncio.TimeoutError:
            game_embed = ds.Embed(color = ds.Color.gold(), description = 'Игра окончена!')
            game_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
            info_message = await ctx.send(embed = game_embed)
            if await self.__del_message(ctx, info_message):
                try:
                    await game_message.delete()
                except ds.NotFound:
                    pass
        else:
            pass
        
def setup(bot):
    bot.add_cog(GamesCog(bot))
