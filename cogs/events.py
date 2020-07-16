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
from discord import logging
import discord as ds
import asyncio
import sqlite3

db  = sqlite3.connect('server.db')
sql = db.cursor()
log = logging.getLogger(__name__)

class EventsCog(commands.Cog, name = 'Events'):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status   = ds.Status.online,
                                       activity = ds.Game(name = "In development on GitHub"))
        log.debug('bot $ Felix runned')
        print('bot $ Felix runned')

    #@commands.Cog.listener()
    #async def on_error(error):
    #    log.error(error)
    #    print(f'[ERROR] {error}', file = sys.stderr)
        
    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        log.info(error)
        print(f'[ERROR] {error}')
        exception = type(error)
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
                               description = f'```css\n{message_error}```',
                               color       = ds.Color.red())
                                    
        error_embed.set_author(name     = 'Упс!',
                               icon_url = ctx.message.author.avatar_url)
                            
        error_embed.set_footer(text = error.__name__)
        error_message = await ctx.send(embed = error_embed)
        await error_message.add_reaction('❔')
    
        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) == '❔'
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check = check_reaction)
        except asyncio.TimeoutError:
            await error_message.remove_reaction('❔', ctx.bot.user)
        else:
            await error_message.remove_reaction('❔', ctx.bot.user)
            error_embed.add_field(name = 'Детали',  value = f'{error.__doc__}',    inline = False)
            error_embed.add_field(name = 'Причина', value = f'{error.__cause__ }', inline = False)
            await error_message.edit(embed = error_embed)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        if data := sql.execute("SELECT role_id FROM emojis WHERE msg_id = ? and emoji = ?", (ctx.message_id,ctx.emoji.name)):
            role = ds.utils.get(ctx.guild.roles, id = data[0][0])
            member = ctx.guild.get_member(ctx.user_id)
            await member.add_roles(role)
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):
        if data := sql.execute("SELECT role_id FROM emojis WHERE msg_id = ? and emoji = ?",(ctx.message_id,ctx.emoji.name)):
            role = ds.utils.get(ctx.guild.roles, id = data[0][0])
            member = ctx.guild.get_member(ctx.user_id)
            await member.remove_roles(role)
    
def setup(bot):
    bot.add_cog(EventsCog(bot))