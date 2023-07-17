import discord
from discord.ext import commands
import json
import random
from data.url import katana, hannah, parker, fletcher, inanimate, nelly, maggie, peeing, great_dane
from data.url import content_dict, rarity_dict
import os

import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

# get token from hidden file
file = open('config.json')
token = json.load(file)

#initalize word dictionary

#function for jumbling words

#initialize client
intents = discord.Intents.all()
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
bot = commands.Bot(command_prefix='$', intents=intents, activity=activity)

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            help_embed = discord.Embed(title="**Help**", description=page, color=discord.Colour.purple())
            await destination.send(embed=help_embed)

bot.help_command = MyNewHelp()


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
@bot.command(name="zuko", brief="Get a random Zuko picture")
async def zuko_pic(ctx):
  global messages
  rand_num = random.randint(0, len(messages)-1)
  msg_num = messages[rand_num].id
  if msg_num in katana:
    await ctx.send(f"{rarity_dict['uncommon']}{content_dict['katana_msg'][random.randint(0, len(content_dict['katana_msg'])-1)]}")
  elif msg_num in parker:
    await ctx.send(f"{rarity_dict['uncommon']}{content_dict['parker_msg'][random.randint(0, len(content_dict['parker_msg'])-1)]}")
  elif msg_num in maggie:
    await ctx.send(f"{rarity_dict['rare']}{content_dict['maggie_msg'][random.randint(0, len(content_dict['maggie_msg'])-1)]}")
  elif msg_num in great_dane:
    await ctx.send(f"{rarity_dict['rare']}{content_dict['great_dane_msg'][random.randint(0, len(content_dict['great_dane_msg'])-1)]}")
  elif msg_num in fletcher:
    await ctx.send(f"{rarity_dict['rare']}{content_dict['fletcher_msg'][random.randint(0, len(content_dict['fletcher_msg'])-1)]}")
  elif msg_num in nelly:
    await ctx.send(f"{rarity_dict['rare']}{content_dict['nelly_msg'][random.randint(0, len(content_dict['nelly_msg'])-1)]}")
  elif msg_num in hannah:
    await ctx.send(f"{rarity_dict['rare']}{content_dict['hannah_msg'][random.randint(0, len(content_dict['hannah_msg'])-1)]}")
  elif msg_num in peeing:
    await ctx.send(f"{rarity_dict['mythical']}{content_dict['peeing_msg'][random.randint(0, len(content_dict['peeing_msg'])-1)]}")
  elif msg_num in inanimate:
    await ctx.send(f"{rarity_dict['mythical']}{content_dict['inanimate_msg'][random.randint(0, len(content_dict['inanimate_msg'])-1)]}")
  await ctx.send(messages[rand_num].attachments[0].url)

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
  if message.author.id == 778145078581133322 and ("MMM" in message.content or "slurp" in message.content.lower() or "suck" in message.content.lower()):
    await message.reply("SLURPY SLURPY SUCKY MMMM SLUCK SUCK SUCKY SLURP SLURP SLURP FOR HAMSTER SUCKER MMMM SLURPY SLURP GLU GLUG")
  if message.author.id == 235857970364153856 and "fraud" in message.content.lower() and "commit" in message.content.lower():
    await message.reply("im calling the police")
  if message.author.id == 588201757633675279 and "taylor swift" in message.content.lower():
    await message.reply("Taylor Swift 😀 feeeaarless 😌 SPEAK NO OW 😫 reeeh (eh ed) 🤓 1989 😐 reputashuunn 😋 loooooveeerrrrrr 😍 folklooree 😕 evermore 😣 MidNights 😜")
  if ("four" in message.content.lower() or "onceler" in message.content.lower()) and ("hot" in message.content.lower() or "daddy" in message.content.lower()):
    await message.reply("the horny police have arrived")
  await bot.process_commands(message)


bot.run(token['token'])