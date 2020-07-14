from discord.ext import commands, tasks
import discord as ds
import sqlite3
import asyncio

#from urllib.request import urlopen
#import git

bot = commands.Bot(command_prefix = "f!")
con = sqlite3.connect('server.db')
sql = con.cursor()

@bot.event
async def on_ready():
    global server
    server = bot.get_guild(728988042987307091)
    print("[ BOT STARTED ]")

@bot.command()
async def card(ctx, member: ds.Member = None):
    if member == None:
        member = ctx.author

    embed  = ds.Embed(title = 'ЛИЧНАЯ КАРТОЧКА', description = member.top_role.mention, colour = ds.Color.red())
    embed.set_author(name = member.name, icon_url = member.avatar_url)
    embed.set_footer(text = bot.user.name, icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url = member.avatar_url)

    for data in sql.execute("SELECT data FROM users WHERE user_id = ?",(member.id,)):
        for args in eval(data[0],{'__builtins__':{}}):
            embed.add_field(**args)
        break
    await ctx.send(embed = embed)

@bot.event
async def on_raw_reaction_add(ctx):
    for data in sql.execute("SELECT role_id FROM emojis WHERE msg_id = ? and emoji = ?",(ctx.message_id,ctx.emoji.name)):
        role = ds.utils.get(server.roles, id = data[0])
        break
    member = server.get_member(ctx.user_id)
    await member.add_roles(role)
    

@bot.event
async def on_raw_reaction_remove(ctx):
    role_id = list(sql.execute("SELECT role_id FROM emojis WHERE msg_id = ? and emoji = ?",(ctx.message_id,ctx.emoji.name)))[0][0]
    role    = ds.utils.get(server.roles, id = role_id)
    member  = server.get_member(ctx.user_id)
    await member.remove_roles(role)
        
bot.run("NzI4OTg4MjIyMjMwNjI2MzEy.XwCZyg.3I5a98uOfsCZvYLir0DJj8NIgt4")

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
