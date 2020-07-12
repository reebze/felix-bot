from oauth2client.service_account import ServiceAccountCredentials as GoogleAccount
from discord.ext import commands, tasks
from settings import settings
import gspread as gsp
import discord as ds
import asyncio

#from urllib.request import urlopen
#import git

bot    = commands.Bot(command_prefix = settings['discord']['prefix'])
client = gsp.authorize(GoogleAccount.from_json_keyfile_dict(settings['database']['token'],settings['database']['scope']))
spreadsheet = client.open('DataBase')


@bot.event
async def on_ready():
    print("[ BOT STARTED ]")
    
    global server
    server = bot.get_guild(settings['discord']['felix_server_id'])

@bot.command(name = 'дай-карточку', aliases = ['дай-карту'])
async def card(ctx, member: ds.Member = None):
    if member == None:
        member = ctx.author

    embed  = ds.Embed(title = 'ЛИЧНАЯ КАРТОЧКА', description = member.top_role.mention, colour = ds.Color.red())
    embed.set_author(name = member.name, icon_url = member.avatar_url)
    embed.set_footer(text = bot.user.name, icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url = member.avatar_url)
    
    sheet = spreadsheet.worksheet('Members')
    for obj in sheet.get_all_records():
        if obj['Member ID'] == member.id:
            for args in eval(obj['Data'],{}):
                embed.add_field(**args)
            break
    await ctx.send(embed = embed)

@bot.event
async def on_raw_reaction_add(ctx):
    sheet = spreadsheet.worksheet('Emoji')
    for obj in sheet.get_all_records():
        if obj['Message ID'] == ctx.message_id and obj['Emoji'] == str(ctx.emoji):
            await server.get_member(ctx.user_id).add_roles(ds.utils.get(server.roles, id = obj['Role ID']))
            break

@bot.event
async def on_raw_reaction_remove(ctx):
    sheet = spreadsheet.worksheet('Emoji')
    for obj in sheet.get_all_records():
        if obj['Message ID'] == ctx.message_id and obj['Emoji'] == str(ctx.emoji):
            await server.get_member(ctx.user_id).remove_roles(ds.utils.get(server.roles, id = obj['Role ID']))
            break
        
bot.run(settings['discord']['token'])

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
