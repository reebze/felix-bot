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
import discord as ds
import asyncio
import sqlite3

db  = sqlite3.connect('server.db')
sql = db.cursor()
log = logging.getLogger(__name__)

class CommandsCog(commands.Cog, name = 'Commands'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'clear')
    @commands.has_permissions(manage_messages=True)
    async def __clear(self, ctx, amount = 5, member: ds.Member = None):
        if amount <= 0:
            embed = ds.Embed(color = ds.Color.red(),title = 'Нарываешься?')
            embed.set_image(url = 'https://media.discordapp.net/attachments/728991407662039140/733423571912753229/flex.png?width=502&height=475')
            await ctx.channel.send(embed = embed)
            return 
        if member == None:
            await ctx.channel.purge(limit = amount + 1) 
        else:
            async for message in ctx.channel.history(limit = amount + 1).filter(lambda message: message.author.id == member.id):
                await message.delete()
        info_message = await ctx.channel.send(embed = ds.Embed(color = ds.Color.gold(),title = 'Сообщения удалены!', description=f'Удалено {amount} сообщений, вызвал {ctx.author.mention}'))
        await info_message.add_reaction('🗑️')
    
        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) == '🗑️'
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=10.0, check = check_reaction)
        except asyncio.TimeoutError:
            await info_message.remove_reaction('🗑️', ctx.bot.user)
        else:
            await info_message.delete()
    
    @commands.command(name = 'clearself')
    async def __clearself(self, ctx, amount = 5):
        if amount <= 0:
            embed = ds.Embed(color = ds.Color.red(),title = 'Нарываешься?')
            embed.set_image(url = 'https://media.discordapp.net/attachments/728991407662039140/733423571912753229/flex.png?width=502&height=475')
            await ctx.channel.send(embed = embed)
            return
        async for message in ctx.channel.history(limit = amount + 1).filter(lambda message: message.author.id == ctx.author.id):
            await message.delete()
        info_message = await ctx.channel.send(embed = ds.Embed(color = ds.Color.gold(),title = 'Сообщения удалены!', description=f'В канале {ctx.channel.mention} удалено {amount} сообщений, вызвал {ctx.author.mention}'))
        await info_message.add_reaction('🗑️')
    
        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) == '🗑️'
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=10.0, check = check_reaction)
        except asyncio.TimeoutError:
            await info_message.remove_reaction('🗑️', ctx.bot.user)
        else:
            await info_message.delete()
                
    
def setup(bot):
    bot.add_cog(CommandsCog(bot))
