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
from discord.ext import commands, tasks
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

class EventsCog(commands.Cog, name = 'Events'):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status   = ds.Status.online,
                                       activity = ds.Game(name = "In development on GitHub"))
        
        sql = db.cursor()                               
        users = list(map(lambda el: el[0], sql.execute('SELECT user_id FROM users')))
        guild = self.bot.get_guild(self.bot.felix_server)
        for member in guild.members:
            if member.id not in users:
                sql.execute('INSERT INTO users (user_id) VALUES (?)', (member.id,))
        db.commit()
        sql.close()
        self.__check_unban.start()
        log.debug('bot $ Felix runned')
        print('bot $ Felix runned')

    async def __del_message(ctx, info_message):
        await info_message.add_reaction('🗑️')

        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) == '🗑️' and user == ctx.message.author
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=10.0, check = check_reaction)
        except asyncio.TimeoutError:
            await info_message.remove_reaction('🗑️', ctx.bot.user)
        else:
            await info_message.delete()
        
    @commands.Cog.listener()
    async def on_error(error):
        log.error(error)
        print(error,end = '\n\n\n')
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log.info(error)
        print(f'[ERROR] {error}')
        exception = type(error)
        message_error = 'Ничего не известно!'
        if exception is commands.errors.MissingPermissions:
            message_error = f'К сожалению, {ctx.message.author.name}, у вас нет прав для этого!'
        elif exception is commands.errors.CheckFailure:
            message_error = f'К сожалению, {ctx.message.author.name}, у вас нет необходимых ролей для этого!'
        elif exception is commands.errors.CommandNotFound:
            message_error = f'К сожалению, {ctx.message.author.name}, такой команды не существует!'
        elif exception is TimeoutError:
            log.warn(f'TimeoutError: {error}')
            return
        
        error_embed = ds.Embed(title       = 'Ошибка',
                               timestamp   = datetime.utcnow(),
                               description = f'```css\n{message_error}```\n{exception.__name__}',
                               color       = ds.Color.red())
                                    
        error_embed.set_author(name     = 'Упс!',
                               icon_url = ctx.message.author.avatar_url)
                               
        error_embed.set_footer(text     = ctx.bot.user.name, 
                               icon_url = ctx.bot.user.avatar_url)
        
        error_message = await ctx.send(embed = error_embed)
        await error_message.add_reaction('❔')
    
        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) == '❔'
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=15.0, check = check_reaction)
        except asyncio.TimeoutError:
            await error_message.remove_reaction('❔', ctx.bot.user)
        else:
            await error_message.remove_reaction('❔', ctx.bot.user)
            error_embed.add_field(name = 'Детали',  value = f'{error.__doc__}',    inline = False)
            error_embed.add_field(name = 'Причина', value = f'{error.__cause__ }', inline = False)
            await error_message.edit(embed = error_embed)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        sql = db.cursor()
        if data := list(sql.execute("SELECT role_id FROM e2r WHERE message_id = ? and emoji_name = ?", (ctx.message_id, ctx.emoji.name))):
            role = ds.utils.get(ctx.bot.get_guild(ctx.guild_id).roles, id = data[0][0])
            member = ctx.guild.get_member(ctx.user_id)
            await member.add_roles(role)
        sql.close()
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):
        sql = db.cursor()
        if data := list(sql.execute("SELECT role_id FROM e2r WHERE message_id = ? and emoji_name = ?", (ctx.message_id, ctx.emoji.name))):
            role = ds.utils.get(ctx.bot.get_guild(ctx.guild_id).roles, id = data[0][0])
            member = ctx.guild.get_member(ctx.user_id)
            await member.remove_roles(role)
        sql.close()
    
    @tasks.loop(minutes=1)
    async def __check_unban(self):
        sql = db.cursor()
        felix = self.bot.get_guild(self.bot.felix_server)
        bans = []
        for row in sql.execute('SELECT user_id, ban_date FROM users WHERE ban_date IS NOT NULL'):
            if row[1] == datetime.now().replace(second = 0, microsecond = 0).timestamp():
                bans.append(row[0])
                
        for id in bans:
            for ban in await felix.bans():
                if ban.user.id == id:
                    await felix.unban(ban.user)
                    sql.execute('UPDATE users SET ban_date = NULL WHERE user_id = ?', (ban.user.id,))
                    db.commit()
                    try:
                        info_embed = ds.Embed(color = ds.Color.gold(), description = 'Вы разбанены на сервере ReyZi')
                        info_embed.set_footer(text = self.bot.user.name, icon_url = self.bot.user.avatar_url)
                        await ban.user.send(embed = info_embed)
                    except:
                        pass
                    info_embed = ds.Embed(color = ds.Color.gold(), description = f'Разбанен {ban.user.name}#{ban.user.discriminator}!')
                    info_embed.set_footer(text = self.bot.user.name, icon_url = self.bot.user.avatar_url)
                    await felix.get_channel(self.bot.felix_channel).send(embed = info_embed)
        sql.close()
        
def setup(bot):
    bot.add_cog(EventsCog(bot))
