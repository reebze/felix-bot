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

__title__     = 'felix-bot/games'
__author__    = ['reebze','Be3y4uu-K0T']
__copyright__ = 'Copyright 2020 (c) 2020 Be3y4uu_K0T'
__license__   = 'MIT'
__version__   = '0.0.1'
__status__    = 'Development'

#======================================
from discord.ext import commands
from contextlib import suppress
from datetime import datetime
from discord import logging
from PIL import Image
from os import walk
import exts.database as db
import discord as ds
import asyncio
import io


logging.basicConfig(filename = r"src\exts\felix.log", 
                    #stream  = sys.stderr,
                    format   = '[%(asctime)s] - %(levelname)s - : %(name)s : %(message)s', 
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
            with suppress(ds.NotFound):
                await info_message.delete()
                await ctx.message.delete()
            return True
        
    @commands.command(name = 'playgame')
    async def __play_in_game(self, ctx):
        game_imgs = {filename[:-4]:Image.open(rf'src\content\{filename}') for filename in tuple(walk(r'src\content'))[0][2] if filename.endswith('.png')}
        count = 5
        game_img = Image.new('RGBA', (count*128,count*128), (32,32,32))
        for coord,img in enumerate(['0g0000_0024','0g0000_0000','0g0000_0023','0g0000_0000','0g0000_0001',
                                    '0g0000_0000','0g0000_0006','0g0000_0011','0g0000_0012','0g0000_0000',
                                    '0g0000_0000','0g0000_0007','0g0003_0000','0g0000_0014','0g0000_0018',
                                    '0g0000_0000','0g0000_0008','0g0000_0009','0g0000_0013','0g0000_0001',
                                    '0g0000_0005','0g0000_0005','0g0000_0003','0g0000_0001','0g0000_0001',]):
            game_img.paste(game_imgs[img],(coord%count * 128,coord//count * 128)) #загрузка плиток
        
        for coord in range(count*count):
            game_img.paste(game_imgs['0g0001_0000'], (coord%count * 128,coord//count * 128) , game_imgs['0g0001_0000']) #эффект старого телевизора

        with io.BytesIO() as img_binary:
            game_img.save(img_binary, format='PNG')
            img_binary.seek(0)
            game_file = ds.File(img_binary, filename = 'main_screen.png')
        game_embed = ds.Embed(color = ds.Color.green(), title = 'Уровень # 1!')
        game_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
        game_message = await ctx.send(embed = game_embed, file = game_file)
        asyncio.gather(*[game_message.add_reaction(emoji) for emoji in '⬅⬆➡⬇🔄'])
        
        def check_reaction(reaction, user):
            return user == ctx.message.author and reaction.message.id == game_message.id and reaction.emoji in '⬅⬆➡⬇🔄'

        async def try_except(function, *exceptions):
            try:
                return await function
            except exceptions:
                return False
            
        with suppress(ds.NotFound):
            while message := await try_except(ctx.fetch_message(game_message.id), ds.NotFound):
                try:
                    reaction, user = await ctx.bot.wait_for('reaction_add', timeout = 125.0, check = check_reaction)
                except asyncio.TimeoutError:
                    game_embed = ds.Embed(color = ds.Color.gold(), description = 'Игра окончена!')
                    game_embed.set_footer(text = ctx.me.name, icon_url = ctx.me.avatar_url)
                    info_message = await ctx.send(embed = game_embed)
                    await self.__del_message(ctx, info_message)
                    await game_message.delete()
                else:
                    pass #пока ещё ничего нет       
        
def setup(bot):
    bot.add_cog(GamesCog(bot))
