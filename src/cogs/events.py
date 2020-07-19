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

__title__     = 'felix-bot/events'
__author__    = ['reebze','Be3y4uu-K0T']
__copyright__ = 'Copyright 2020 (c) 2020 Be3y4uu_K0T'
__license__   = 'MIT'
__version__   = '0.1.3'
__status__    = 'Development'

#======================================
from discord.ext import commands, tasks
from datetime import datetime
from discord import logging
import exts.database as db
import discord as ds
import asyncio

logging.basicConfig(filename = r"src\exts\felix.log", 
                    #stream  = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s - : %(name)s : %(message)s', 
                    datefmt  = '%d/%m/%Y#%H:%M:%S')
log = logging.getLogger(__name__)

class EventsCog(commands.Cog, name = 'Events'):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status   = ds.Status.online,
                                       activity = ds.Game(name = "In development on GitHub"))
        
        with db.sql() as sql:                            
            users = list(map(lambda el: el[0], sql.execute('SELECT user_id FROM users')))
            guild = self.bot.get_guild(self.bot.felix_server)
            for member in guild.members:
                if member.id not in users:
                    sql.execute('INSERT INTO users (user_id,art_points) VALUES (?,?)', (member.id,0))
        self.__check_unban.start()
        log.info('bot $ Felix runned')
        print('bot $ Felix runned')

    @commands.Cog.listener()
    async def on_disconnect(self):
        log.info('bot $ Felix disconnected to discord')
        print('bot $ Felix disconnected to discord')
        
    @commands.Cog.listener()
    async def on_connect(self):
        log.info('bot $ Felix connected to discord')
        print('bot $ Felix connected to discord')
        
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
        
    @commands.Cog.listener()
    async def on_error(error):
        log.error(error)
        print(error,end = '\n\n\n')
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log.info(error)
        print(f'[ERROR] {error}')
        exception = type(error)
        message_error = 'Внутренняя ошибка сервера!'
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
                               
        error_embed.set_footer(text     = ctx.me.name, 
                               icon_url = ctx.me.avatar_url)
        
        error_message = await ctx.send(embed = error_embed)
        await error_message.add_reaction('❔')
        await error_message.add_reaction('🗑️')
    
        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) in ['❔','🗑️']
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=10.0, check = check_reaction)
        except asyncio.TimeoutError:
            await error_message.remove_reaction('❔', ctx.bot.user)
            await error_message.remove_reaction('🗑️', ctx.bot.user)
        else:
            if str(reaction.emoji) == '❔':
                await error_message.remove_reaction('❔', ctx.bot.user)
                await error_message.remove_reaction('🗑️', ctx.bot.user)
                error_embed.add_field(name = 'Детали',  value = f'{error.__doc__}',    inline = False)
                error_embed.add_field(name = 'Причина', value = f'{error.__cause__ }', inline = False)
                error_message = await error_message.edit(embed = error_embed)
                await self.__del_message(ctx, error_message)
            else:
                await ctx.message.delete()
                await error_message.delete()
         
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.channel.id == 732589225085763586:
            '''
            Картинка : (png/jpg/jepg)      => AP+1
            Музыка   : (mp3/wav/ogg)       => AP+3
            Анимация : (mp4/webm/gif/gifv) => AP+5
            Лайк     : (emoji)             => AP+1
            '''
            ArtPs = sum(map(lambda ctx: {'png' : 1, 'jpg' : 1, 'jepg' : 1, 
                                         'mp3' : 3, 'wav' : 3, 'ogg'  : 3,
                                         'mp4' : 5, 'gif' : 5, 'gifv' : 5, 'webm' : 5
                                        }.get(ctx.filename.split('.')[-1].lower(),0), message.attachments))
            if ArtPs > 0:
                with db.sql() as sql:
                    ArtPs += list(sql.execute('SELECT art_points FROM users WHERE user_id = ?', (message.author.id,)))[0][0]
                    sql.execute('UPDATE users SET art_points = ? WHERE user_id = ?', (ArtPs,message.author.id))
                #emoji = get(self.bot.get_all_emojis(), name='Art_Like')
                await message.add_reaction('💟')
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx): 
        with db.sql() as sql:
            if data := list(sql.execute("SELECT role_id FROM e2r WHERE message_id = ? and emoji_name = ?", (ctx.message_id, ctx.emoji.name))):
                role = ds.utils.get(ctx.bot.get_guild(ctx.guild_id).roles, id = data[0][0])
                member = ctx.guild.get_member(ctx.user_id)
                await member.add_roles(role)
            elif ctx.emoji.name == '💟' and ctx.channel_id == 732589225085763586 and ctx.user_id != self.bot.user.id:
                message = await self.bot.get_guild(self.bot.felix_server).get_channel(ctx.channel_id).fetch_message(ctx.message_id)
                ArtPs = list(sql.execute('SELECT art_points FROM users WHERE user_id = ?', (message.author.id,)))[0][0] + 1
                sql.execute('UPDATE users SET art_points = ? WHERE user_id = ?', (ArtPs,message.author.id))
                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):
        with db.sql() as sql:
            if data := list(sql.execute("SELECT role_id FROM e2r WHERE message_id = ? and emoji_name = ?", (ctx.message_id, ctx.emoji.name))):
                role = ds.utils.get(ctx.bot.get_guild(ctx.guild_id).roles, id = data[0][0])
                member = ctx.guild.get_member(ctx.user_id)
                await member.remove_roles(role)
            elif ctx.emoji.name == '💟' and ctx.channel_id == 732589225085763586 and ctx.user_id != self.bot.user.id:
                message = await self.bot.get_guild(self.bot.felix_server).get_channel(ctx.channel_id).fetch_message(ctx.message_id)
                ArtPs = list(sql.execute('SELECT art_points FROM users WHERE user_id = ?', (message.author.id,)))[0][0] - 1
                sql.execute('UPDATE users SET art_points = ? WHERE user_id = ?', (ArtPs,message.author.id))
    
    @tasks.loop(minutes=1)
    async def __check_unban(self):
        with db.sql() as sql:
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
                        sql.commit()
                        try:
                            info_embed = ds.Embed(color = ds.Color.gold(), description = 'Вы разбанены на сервере ReyZi!')
                            info_embed.set_footer(text = self.bot.user.name, icon_url = self.bot.user.avatar_url)
                            await ban.user.send(embed = info_embed)
                        except:
                            pass
                        info_embed = ds.Embed(color = ds.Color.gold(), description = f'Разбанен {ban.user.name}#{ban.user.discriminator}!')
                        info_embed.set_footer(text = self.bot.user.name, icon_url = self.bot.user.avatar_url)
                        await felix.get_channel(self.bot.felix_channel).send(embed = info_embed)
        
def setup(bot):
    bot.add_cog(EventsCog(bot))