import discord
from discord.ext import commands
import json
import random

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

loaded = False
messages = []

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
  global loaded, messages
  if not loaded:
    await bot.load_extension("ext.anagram")
    channel = bot.get_channel(1121079217774407750)
    messages = [message async for message in channel.history(limit=700)]
    print(len(messages))
    loaded = True
    print("loading up...")
    

#generates a random zuko picture from zuko-pics-database channel
@bot.command(name="zuko")
async def zuko_pic(ctx):
  global messages
  msg_num = random.randint(0, len(messages)-1)
  await ctx.send(messages[msg_num].attachments[0].url)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.author.id == 218500036995055617 and "yass" in message.content.lower():
    await message.reply("YASS QUEEN!!!")
  if message.author.id == 274004148276690944 and "pee" in message.content.lower():
    global pee_ctr
    await message.reply(f"bren pee counter: {pee_ctr} (yet)")
    pee_ctr+=1
  if message.author.id == 778145078581133322 and "MMM" in message.content:
    await message.reply("SLURPY SLURPY SUCKY MMMM SLUCK SUCK SUCKY SLURP SLURP SLURP FOR HAMSTER SUCKER MMMM SLURPY SLURP GLU GLUG")
  if message.author.id == 235857970364153856 and "fraud" in message.content.lower() and "commit" in message.content.lower():
    await message.reply("im calling the police")
  if message.author.id == 588201757633675279 and "taylor swift" in message.content.lower():
    await message.reply("Taylor Swift 😀 feeeaarless 😌 SPEAK NO OW 😫 reeeh (eh ed) 🤓 1989 😐 reputashuunn 😋 loooooveeerrrrrr 😍 folklooree 😕 evermore 😣 MidNights 😜")
  if ("four" in message.content.lower() or "onceler" in message.content.lower()) and ("hot" in message.content.lower() or "daddy" in message.content.lower()):
    await message.reply("the horny police have arrived")
  await bot.process_commands(message)


bot.run(token['token'])