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
logging.basicConfig(filename = "felix.log", 
                    #stream   = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s] - : %(name)s : %(message)s', 
                    datefmt  ='%d/%m/%Y#%H:%M:%S')
log = logging.getLogger(__name__)

class CommandsCog(commands.Cog, name = 'Commands'):

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
        else:
            await info_message.delete()
            try:
                await ctx.message.delete()
            except:
                pass
        
    @commands.command(name = 'clear')
    @commands.has_permissions(manage_messages=True)
    async def __clear(self, ctx, amount = 5, member: ds.Member = None):
        if amount <= 0:
            embed = ds.Embed(color = ds.Color.red(),title = 'Нарываешься?')
            embed.set_image(url = 'https://media.discordapp.net/attachments/728991407662039140/733423571912753229/flex.png?width=502&height=475')
            await ctx.channel.send(embed = embed)
            return
        await ctx.message.delete()
        if member == None:
            await ctx.channel.purge(limit = amount)
        else:
            async for message in ctx.channel.history(limit = amount).filter(lambda message: message.author.id == member.id):
                await message.delete()
        message = await ctx.channel.send(embed = ds.Embed(color = ds.Color.gold(), title = 'Сообщения удалены!', description=f'Удалено {amount} сообщений, вызвал {ctx.author.mention}'))
        await self.__del_message(ctx, message)

    @commands.command(name = 'clearself')
    async def __clearself(self, ctx, amount = 5):
        if amount <= 0:
            embed = ds.Embed(color = ds.Color.red(),title = 'Нарываешься?')
            embed.set_image(url = 'https://media.discordapp.net/attachments/728991407662039140/733423571912753229/flex.png?width=502&height=475')
            await ctx.channel.send(embed = embed)
            return
        await ctx.message.delete()
        async for message in ctx.channel.history(limit = amount).filter(lambda message: message.author.id == ctx.author.id):
            await message.delete()
        info_embed = ds.Embed(color = ds.Color.gold(), title = 'Сообщения удалены!', description=f'В канале {ctx.channel.mention} удалено {amount} сообщений, вызвал {ctx.author.mention}')
        info_embed.set_footer(text = ctx.bot.user.name, icon_url = ctx.bot.user.avatar_url)
        message = await ctx.channel.send(embed = info_embed)
        await self.__del_message(ctx, message)

    @commands.command(name = 'kick')
    @commands.has_permissions(kick_members=True)
    async def __kick(self, ctx, member: ds.Member, *, reason = None):
        await member.kick(reason = reason)
        info_embed = ds.Embed(color = ds.Color.gold(), title = f'Кикнут {ban.user.name}#{ban.user.discriminator}!', description = f'Причина: {reason}')
        info_embed.set_thumbnail(url = member.avatar_url)
        info_embed.set_footer(text = ctx.bot.user.name, icon_url = ctx.bot.user.avatar_url)
        message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)

    @commands.command(name = 'ban')
    @commands.has_permissions(ban_members=True)
    async def __ban(self, ctx, member: ds.Member, *, reason = None):
        await member.ban(reason = reason)
        info_embed = ds.Embed(title = f'Забенен {ban.user.name}#{ban.user.discriminator}!', description = f'Причина: {reason}')
        info_embed.set_thumbnail(url = member.avatar_url)
        info_embed.set_footer(text = ctx.bot.user.name, icon_url = ctx.bot.user.avatar_url)
        message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)

    @commands.command(name = 'unban')
    @commands.has_permissions(ban_members=True)
    async def __unban(self, ctx, *, member):
        for ban in await ctx.guild.bans():
            if (ban.user.name,ban.user.discriminator) == tuple(member.split('#')):
                await ctx.guild.unban(ban.user)
                info_embed = ds.Embed(color = ds.Color.gold(), description = f'Разбанен {ban.user.name}#{ban.user.discriminator}!')
                info_embed.set_footer(text = ctx.bot.user.name, icon_url = ctx.bot.user.avatar_url)
                message = await ctx.send(embed = info_embed)
                await self.__del_message(ctx, message)
                return
        info_embed = ds.Embed(color = ds.Color.gold(), description = 'Такой пользователь не забанен или не существует его!')
        info_embed.set_footer(text = ctx.bot.user.name, icon_url = ctx.bot.user.avatar_url)
        message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)
        
    @commands.command(name = 'bantime')
    @commands.has_permissions(ban_members=True)
    async def __bantime(self, ctx, member: ds.Member, date: (lambda d: datetime.strptime(d, '%d/%m/%y %H:%M').timestamp()), *, reason = None):
        await member.ban(reason = reason)
        sql = db.cursor()
        sql.execute('UPDATE users SET ban_date = ? WHERE user_id = ?', (date, member.id))
        db.commit()
        sql.close()
        info_embed = ds.Embed(title = f'Забенен {ban.user.name}#{ban.user.discriminator}!', description = f'Причина: {reason}')
        info_embed.set_thumbnail(url = member.avatar_url)
        info_embed.set_footer(text = ctx.bot.user.name, icon_url = ctx.bot.user.avatar_url)
        message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)
        
    @commands.command(name = 'utcnow')
    async def __utcnow(self, ctx):
        info_embed = ds.Embed(description = f'Сейчас по UTC: {datetime.utcnow()}')
        info_embed.set_footer(text = ctx.bot.user.name, icon_url = ctx.bot.user.avatar_url)
        message = await ctx.send(embed = info_embed)
        await self.__del_message(ctx, message)
        
    @commands.command(name = 'e2r')
    @commands.has_permissions(administrator=True)
    async def __e2r(self, ctx):
        pass

def setup(bot):
    bot.add_cog(CommandsCog(bot))
