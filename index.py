from discord.ext import commands, tasks
from urllib.request import urlopen
from oauth2client.service_account import ServiceAccountCredentials
import gspread as gsp
import discord as ds
import json
import git

with open('info.json') as json_file:
    data_info = json.load(json_file)

bot    = commands.Bot(command_prefix = data_info['prefix'])
server = bot.get_guild(data_info['felix_server_id'])
scope  = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds  = ServiceAccountCredentials.from_json_keyfile_dict(data_info['google_drvie'], scope)
client = gsp.authorize(creds)
db     = client.open(json_file['db'])

@tasks.loop(hours=24)
async def updates():
    data = urlopen("https://raw.githubusercontent.com/reebze/felix-bot/master/.version") #пока не может отправлять запрос, потому что репозиторий закрыт
    for line in data:
        new_ver = line.decode()
        break
    new_ver.rstrip("\n").rstrip("\r")
    if new_ver > __version__:
        pass #загрузка новой версии с github
    
@bot.command(name = 'дай-карточку', aliases = ['дай-карту'])
async def card(ctx, person: ds.Member = None):
    if person == None:
        person = ctx.author
    
    role   = str(person.top_role.mention)
    if role == '<@&728988042987307091>':
        role = '---'
    
    rank   = 34 #получать из database google drive (db)
    level  = 2  #так же оттуда
    xp     = 394 #db 
    xp_max = 2300 #db
    embed  = ds.Embed(title = 'ЛИЧНАЯ КАРТОЧКА', description = role,colour = ds.Color.red())
    embed.set_author(name = person.name, icon_url = person.avatar_url)
    embed.set_footer(text = bot.user.name, icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url = person.avatar_url) 
    embed.add_field(name = 'РАНГ', value = f'#{rank}')
    embed.add_field(name = 'ЛВЛ', value = f'%{level}')
    embed.add_field(name = 'ОПЫТ', value = f'%{xp}/{xp_max}')

    await ctx.send(embed = embed)

@bot.event
async def on_raw_reaction_add(ctx):
    #todo write
    #if role := db['reaction_dict'][ctx.message_id].get(str(ctx.emoji)) != None:
    #   await server.get_member(ctx.user_id).add_roles(role)
    
    Role = None
    ID = 729012187300888697
    if ctx.message_id != ID:
        return
    if str(ctx.emoji) == "🎮":
        Role = ds.utils.get(felix.roles, id = 729011989581660160)
    if str(ctx.emoji) == "🃏":
        Role = ds.utils.get(felix.roles, id = 729012026646724619)    
    if Role != None:
        await server.get_member(ctx.user_id).add_roles(Role)

@bot.event
async def on_raw_reaction_remove(ctx):
    #todo write 
    #if role := db['reaction_dict'][ctx.message_id].get(str(ctx.emoji)) != None:
    #   await server.get_member(ctx.user_id).remove_roles(role)
    
    Role = None
    ID = 729012187300888697
    if ctx.message_id != ID:
        return
    if str(ctx.emoji) == "🎮":
        Role = ds.utils.get(felix.roles, id = 729011989581660160)
    if str(ctx.emoji) == "🃏":
        Role = ds.utils.get(felix.roles, id = 729012026646724619)        
    if Role != None:
        await server.get_member(ctx.user_id).remove_roles(Role)


@bot.event
async def on_ready():
    print("[ BOT STARTED ]")
    
    updates.start()
