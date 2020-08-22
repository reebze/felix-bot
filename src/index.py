# -*- coding: utf-8 -*-
"""Usage:
  index.py run <token> [<file-db>] [<prefix>] 
  index.py (options)

Arguments:
  <token>        Set token bot.
  <prefix>       Set prefix bot [defualt: f!].
  <file-db>      Set path to file database [defualt: ./server.db]

Options:
  -h, --help     Show this screen.
  -v, --version  Show version.
"""
__license__ = \
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
__version__   = '0.2.8a'
__status__    = 'Development'
#===============[References]============
from discord.ext import commands, tasks
from datetime import datetime
from docopt import docopt
from PIL import Image
from os import walk
import discord as ds
import youtube_dl
import contextlib 
import asyncio
import sqlite3
import sys
import io
#================[Args]=================
args = docopt(__doc__, version=__version__)
if not (args['<token>'] and args['<prefix>'] and args['<file db>']):
    exit(1)
#================[Bot]==================
bot = commands.Bot(command_prefix=args['<prefix>'], help_command=None, owner_ids={427854075099348993})
bot.config = config = {
    'server_id': 728988042987307091,
    'bot_channel_id': 728991407662039140,
    'art_channel_id': 732589225085763586,
}
#==============[DataBase]===============
db = sqlite3.connect(args['<file-db>'])
@contextlib.contextmanager
def sql():
    global db
    sql_cursor = db.cursor()
    try:
        yield sql_cursor
    finally:
        sql_cursor.close()
        db.commit()
#=======================================
@bot.event
async def on_ready():
    await bot.change_presence(status=ds.Status.online, activity=ds.Game(name="In development on GitHub"))
    with sql() as cur:
        guild_member_ids = set(map(lambda member: member.id, bot.get_guild(bot.config['server_id']).members))
        db_member_ids = set(map(lambda member: member[0], cur.execute('SELECT member_id FROM members')))
        new_member_ids = (guild_member_ids | db_member_ids) - (guild_member_ids & db_member_ids)
        for member_id in new_member_ids:
            cur.execute('INSERT INTO users (user_id,art_points) VALUES (?,?)', [member_id,0])
            print(f'$ BOT: New member add ID => {member_id}')

@bot.event
async def on_connect():
    print('bot $ Felix connected to discord!')

@bot.event
async def on_disconnect():
    print('$ BOT: Felix disconnected to discord!')

@bot.event
async def on_error(error):
    print(f'$ ERR: {error}')

@bot.event
async def on_command_error(ctx, error):
    print(f'$ ERR: {error}')
    if type(error) is commands.MissingPermissions:
        text = f'К сожалению, {ctx.message.author.name}, у Вас нет необходимых прав для этого!'
    elif type(error) is commands.MissingRole:
        text = f'К сожалению, {ctx.message.author.name}, у Вас нет необходимых ролей для этого!'
    elif type(error) is commands.CommandNotFound:
        text = f'К сожалению, {ctx.message.author.name}, такой команды не существует!'
    elif type(error) is commands.BadArgument:
        text = f'К сожалению, {ctx.message.author.name}, Вы допустили ошибку в аргументах!'
    elif type(error) is commands.PrivateMessageOnly:
        text = f'К сожалению, {ctx.message.author.name}, команда доступна только в личных сообщениях!'
    elif type(error) is commands.NoPrivateMessage:
        text = f'К сожалению, {ctx.message.author.name}, команда доступна только на сервере!'
    elif type(error) is commands.DisabledCommand:
        text = f'К сожалению, {ctx.message.author.name}, данная команда отключена!'
    elif type(error) is commands.CommandInvokeError:
        text = f'К сожалению, {ctx.message.author.name}, в данной команде произошла ошибка!'
    elif type(error) is TimeoutError:
        text = 'TimeoutError: Ошибка времени выполнения!'
    elif type(error) is RuntimeError:
        text = 'RuntimeError: Ошибка времени выполнения!'
    else:
        text = '$500: Internal Server Error'
    embed = await defualt_embed(title='ERROR', description=text)
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == bot.config['art_channel_id']:
        '''
        Картинка : (png/jpg/jepg)      => AP+1
        Музыка   : (mp3/wav/ogg)       => AP+3
        Анимация : (mp4/webm/gif/gifv) => AP+5
        Лайк     : (emoji)             => AP+1
        '''
        art_points = sum(map(lambda ctx: {'png' : 1, 'jpg' : 1, 'jepg' : 1, 
                                     'mp3' : 3, 'wav' : 3, 'ogg'  : 3,
                                     'mp4' : 5, 'gif' : 5, 'gifv' : 5, 'webm' : 5
                                    }.get(ctx.filename.split('.')[-1].lower(),0), message.attachments))
        if art_points > 0:
            with sql() as cur:
                cur.execute('UPDATE members SET art_points=art_points+? WHERE member_id=?', (message.author.id, art_points))
            #emoji = get(self.bot.get_all_emojis(), name='Art_Like')
            await message.add_reaction('💟')

@bot.event
async def on_raw_reaction_add(ctx):
    if ctx.user_id == bot.user.id:
        return
    with sql() as cur:
        guild = bot.get_guild(bot.config['server_id'])
        if data := list(cur.execute('SELECT role_id FROM emoji_to _role WHERE message_id=? and emoji_name=?', [ctx.message_id, ctx.emoji.name])):
            role = ds.utils.get(guild.roles, id=data[0][0])
            member = guild.get_member(ctx.user_id)
            await member.add_roles(role)
        elif ctx.channel_id == bot.config['art_channel_id'] and ctx.emoji.name == '💟':
            message = await guild.get_channel(ctx.channel_id).fetch_message(ctx.message_id)
            cur.execute('UPDATE members SET art_points=art_points+1 WHERE member_id=?', [message.author.id])

@bot.event
async def on_raw_reaction_remove(ctx):
    if ctx.user_id == bot.user.id:
        return
    with sql() as cur:
        guild = bot.get_guild(bot.config['server_id'])
        if data := list(cur.execute('SELECT role_id FROM emoji_to _role WHERE message_id=? and emoji_name=?', [ctx.message_id, ctx.emoji.name])):
            role = ds.utils.get(guild.roles, id=data[0][0])
            member = guild.get_member(ctx.user_id)
            await member.remove_roles(role)
        elif ctx.channel_id == bot.config['art_channel_id'] and ctx.emoji.name == '💟':
            message = await guild.get_channel(ctx.channel_id).fetch_message(ctx.message_id)
            cur.execute('UPDATE members SET art_points=art_points-1 WHERE member_id=?', [message.author.id])

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: abs=5, member: ds.Member=None):
    await ctx.message.delete()
    if member != None:
        member = (lambda message: message.author.id == member.id)
    await ctx.channel.purge(limit=amount, check=member)
    embed = await defualt_embed(title='Сообщения удалены!', description=f'Удалено {amount} сообщений, вызвал {ctx.author.mention}')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
async def clearself(ctx, amount: abs=5):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount, check=(lambda message: message.author.id == ctx.author.id))
    embed = await defualt_embed(title='Сообщения удалены!', description=f'Удалено {amount} сообщений, вызвал {ctx.author.mention}')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: ds.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = await defualt_embed(title=f'Кикнут {ban.user}!', description=f'Причина: {reason}')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: ds.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = await defualt_embed(title=f'Забенен {ban.user}!', description=f'Причина: {reason}')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member, *, reason=None):
    guild = bot.get_guild(bot.config['server_id'])
    for ban in await ctx.guild.bans():
        if str(ban.user) == member:
            await guild.unban(ban.user, reason=reason)
            with sql() as cur:
                cur.execute('UPDATE members SET ban_date=NULL WHERE member_id=?',[ban.user.id])
            embed = await defualt_embed(description=f'{ban.user} был разбанен!')
            message = await ctx.send(embed=embed)
            await delete_message(ctx, message)
            return
    embed = await defualt_embed(description='Такой пользователь не заблокирован, или он не существует!')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
@commands.has_permissions(ban_members=True)
async def bantime(ctx, member: ds.Member, date: (lambda _: datetime.strptime(_, '%d/%m/%Y %H:%M').timestamp()), *, reason=None):
    await member.ban(reason=reason)
    with sql() as cur:
        cur.execute('UPDATE members SET ban_date=? WHERE member_id=?',[date, member.id])
    embed = await defualt_embed(title=f'Забенен {ban.user} до {datetime.fromtimestamp(date)}!', description=f'Причина: {reason}')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
async def utcnow(ctx):
    embed = await defualt_embed(description=f'Сейчас по UTC: {datetime.utcnow()}')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
async def now(ctx):
    embed = await defualt_embed(description=f'Сейчас по МСК+2: {datetime.now()}')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
@commands.has_permissions(administrator=True)
async def emoji2role(ctx):
    pass

@bot.command()
async def palygame(ctx):
    imgs = {filename[:-4]:Image.open(rf'src\content\{filename}') for filename in tuple(walk(r'src\content'))[0][2] if filename.endswith('.png')}
    size = 5
    img = Image.new('RGBA', (size*128,size*128), (32,32,32))
    for coord,frame in enumerate(['0g0000_0024','0g0000_0000','0g0000_0023','0g0000_0000','0g0000_0001',
                                '0g0000_0000','0g0000_0006','0g0000_0011','0g0000_0012','0g0000_0000',
                                '0g0000_0000','0g0000_0007','0g0003_0000','0g0000_0014','0g0000_0018',
                                '0g0000_0000','0g0000_0008','0g0000_0009','0g0000_0013','0g0000_0001',
                                '0g0000_0005','0g0000_0005','0g0000_0003','0g0000_0001','0g0000_0001',]):
        img.paste(imgs[frame],(coord%size * 128,coord//size * 128)) #загрузка плиток

    hash_img = Image.new('RGBA', (size*128,size*128), (32,32,32))
    for coord in range(size**2):
        hash_img.paste(imgs['0g0001_0000'], (coord%size * 128,coord//size * 128))

    frame_one = Image.alpha_composite(img,hash_img) #эффект старого телевизора
    frame_two = Image.alpha_composite(img,hash_img.rotate(180)) #эффект старого телевизора

    with io.BytesIO() as img_binary:
        frame_one.save(img_binary, format='GIF', save_all=True, append_images=[frame_two,frame_two]*15+[frame_one]*10, optimize=False, duration=40, loop=0)
        #img.save(img_binary, format='PNG')
        img_binary.seek(0)
        file = ds.File(img_binary, filename='main_screen.gif')

    embed = await defualt_embed(title='Уровень #1!')
    message = await ctx.send(embed=embed, file=file)
    asyncio.gather(*[message.add_reaction(emoji) for emoji in '⬅⬆➡⬇🔄'])

    def func_check(reaction, member):
        return member == ctx.message.author and str(reaction.emoji) in '⬅⬆➡⬇🔄' and reaction.message.id == message.id

    async def try_except(function, *exceptions):
        try:
            return await function
        except exceptions:
            return False

    with contextlib.suppress(ds.NotFound):
        while message := await try_except(ctx.fetch_message(message.id), ds.NotFound):
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=125.0, check=func_check)
            except asyncio.TimeoutError:
                await message.delete()
                embed = await defualt_embed(description='Игра окончена!')
                message = await ctx.send(embed=embed)
                await delete_message(ctx, message)
            else:
                reaction, user #пока ещё ничего нет  

@bot.command()
#@commands.has_role()
@commands.has_permissions(administrator=True)
async def join(self, ctx):
    try:
        await ctx.message.author.voice.channel.connect()
    except AttributeError:
        embed = await defualt_embed(description='Вы не находитесь в голосовом канале!')
        message = await ctx.send(embed=embed)
    else:
        embed = await defualt_embed(description=f'{bot.user.name}  подключился к #{ctx.message.author.voice.channel.name}')
        message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
#@commands.has_role()
@commands.has_permissions(administrator=True)
async def __leave_channel(self, ctx):
    try:
        await ctx.voice_client.disconnect()
    except AttributeError:
        embed = await defualt_embed(description=f'{bot.user.name} не подключен к голосовому каналу!')
        message = await ctx.send(embed=embed)
    else:
        embed = await defualt_embed(description=f'{bot.user.name}  отключился от #{ctx.message.author.voice.channel.name}')
        message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@bot.command()
#@commands.has_role()
@commands.has_permissions(administrator=True)
async def __play(self, ctx):
    ctx.voice_client.play(ds.FFmpegPCMAudio(r".\the_final_station_14_nowhere_town.mp3"), after=lambda e: print('Конец, возможная ошибка:', e))
    embed = await defualt_embed(description=f'Шарманка запущена!')
    message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@commands.command()
#@commands.has_role()
@commands.has_permissions(administrator=True)
async def __stop(self, ctx):
    try:
        ctx.voice_client.stop()
    except AttributeError:
        embed = await defualt_embed(description=f'Бот не находится в голосовом канале!')
        message = await ctx.send(embed=embed)
    else:
        embed = await defualt_embed(description=f'Шарманка остановлена!')
        message = await ctx.send(embed=embed)
    await delete_message(ctx, message)
        
@commands.command()
#@commands.has_role()
@commands.has_permissions(administrator=True)
async def __pause(self, ctx):
    try:
        ctx.voice_client.pause()
    except AttributeError:
        embed = await defualt_embed(description=f'Бот не находится в голосовом канале!')
        message = await ctx.send(embed=embed)
    else:
        embed = await defualt_embed(description=f'Шарманка приостановлена!')
        message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@commands.command()
#@commands.has_role()
@commands.has_permissions(administrator=True)
async def __resume(self, ctx):
    try:
        ctx.voice_client.resume()
    except AttributeError:
        embed = await defualt_embed(description=f'Бот не находится в голосовом канале!')
        message = await ctx.send(embed=embed)
    else:
        embed = await defualt_embed(description=f'Шарманка продолжает играть!')
        message = await ctx.send(embed=embed)
    await delete_message(ctx, message)

@tasks.loop(minutes=1)
async def check_unban():
    with sql() as cur:
        guild = bot.get_guild(bot.config['server_id'])
        date = datetime.now().replace(second = 0, microsecond = 0).timestamp()
        data = cur.execute('SELECT ban_date FROM members WHERE ban_date=?', [date])
        ids = set(map(lambda member: member[0], data))
        for ban in await guild.bans():
            if ban.user.id in ids:
                await guild.unban(ban.user, reason = 'Истек срок бана.')
                cur.execute('UPDATE members SET ban_date = NULL WHERE member_id = ?', [ban.user.id])
                embed = await defualt_embed(title='INFO', description=f'Разбанен {ban.user}!') 
                await guild.get_channel(bot.config['bot_channel_id']).send(embed=embed) 

async def defualt_embed(**args):
    embed = ds.Embed(color = ds.Colour.purple(), **args)
    embed.set_footer(text = bot.user.name, icon_url = bot.user.avatar_url)
    return embed

async def delete_message(ctx, message):
    def func_check(reaction, member):
        return member == ctx.message.author and str(reaction.emoji) == '🔥' and reaction.message.id == message.id

    with contextlib.suppress(ds.NotFound):
        try:
            await message.add_reaction('🔥')
            await bot.wait_for('reaction_add', timeout=10.0, check=func_check)
        except asyncio.TimeoutError:
            await message.remove_reaction('🔥', bot.user)
        else:
            await message.delete()
            await ctx.message.delete()
            return True
    return False
#================[Main]=================
if __name__ == "__main__":
    bot.run(args['<token>'], bot = True, reconnect = True)
    print('$ BOT: Felix-Bot has been started!')