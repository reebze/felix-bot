from discord.ext import commands, tasks
from urllib.request import urlopen
from oauth2client.service_account import ServiceAccountCredentials
import discord as ds
import json
import gspread as gsp

with open('info.json') as json_file:
    data_info = json.load(json_file)


bot    = commands.Bot(command_prefix = data_info['prefix'])
server = bot.get_guild(data_info['felix_server_id'])
scope  = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds  = ServiceAccountCredentials.from_json_keyfile_dict(data_info['google_drvie'], scope)
client = gsp.authorize(creds)
db     = client.open(json_file['db'])

#https://raw.githubusercontent.com/reebze/felix-bot/master/.version?token=AOKP4SVG6DDU6FUHHBFEBFC7AH47U
