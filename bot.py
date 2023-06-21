import discord
from discord.ext import commands
import json

#global anagram variables
anagram_game_started = False
anagram_game_finished = False
anagram_jumbled = ""
anagram_normal = ""
anagram_players = []

# get token from hidden file
file = open('config.json')
token = json.load(file)

#initalize word dictionary

#function for jumbling words

#initialize client
intents = discord.Intents.default()
intents.message_content = True



#initialize bot commands
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

cogs = [
  "ext.anagram"
]

activity = discord.Game(name="$anagram")

bot = commands.Bot(command_prefix='$', intents=intents,  help_command = help_command, activity=activity)

@bot.event
async def on_ready():
  print("loading up...")
  await bot.load_extension("ext.anagram")

@bot.command(name="zuko")
async def zuko_pic(ctx):
  channel = bot.get_channel(1121079217774407750)
  messages = [message async for message in channel.history(limit=123)]
  print(messages)
  await ctx.send(messages[0].attachments[0].url)

bot.run(token['token'])