from discord.ext import commands, tasks
import discord as ds

#from urllib.request import urlopen
#import git

from settings import settings

bot = commands.Bot(command_prefix = settings['discord']['prefix'])

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

@bot.command(name = 'дай-карточку', aliases = ['дай-карту'])
async def card(ctx, person: ds.Member = None):
    if person == None:
        person = ctx.author
        
    embed  = ds.Embed(title = 'ЛИЧНАЯ КАРТОЧКА', description = person.top_role.mention, colour = ds.Color.red())
    embed.set_author(name = person.name, icon_url = person.avatar_url)
    embed.set_footer(text = bot.user.name, icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url = person.avatar_url)
    if (member := settings['database']['Members'].get(person.id)) != None:
        for field in member:
            if type(field['val']) is list:
                embed.add_field(name = field['name'], value = f"{field['prefix']}{'/'.join(map(str,field['val']))}" )
            else:
                embed.add_field(name = field['name'], value = f"{field['prefix']}{field['val']}" )
    await ctx.send(embed = embed)

@bot.event
async def on_raw_reaction_add(ctx):
    if (role := settings['database']['Emoji'].get(ctx.message_id, {}).get(str(ctx.emoji))) != None:
        await server.get_member(ctx.user_id).add_roles(ds.utils.get(server.roles, id = role))

@bot.event
async def on_raw_reaction_remove(ctx):
    if (role := settings['database']['Emoji'].get(ctx.message_id, {}).get(str(ctx.emoji))) != None:
        await server.get_member(ctx.user_id).remove_roles(ds.utils.get(server.roles, id = role))

@bot.event
async def on_ready():
    print("[ BOT STARTED ]")
    
    global server
    server = bot.get_guild(settings['discord']['felix_server_id'])

bot.run(settings['discord']['token'])
