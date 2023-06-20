import discord
from discord.ext import commands
from random_word import Wordnik
import random
import json
import asyncio

anagram_game_started = False
anagram_game_finished = False
anagram_jumbled = ""
anagram_normal = ""
anagram_players = []

# get token from hidden file
file = open('config.json')
token = json.load(file)

#initalize word dictionary
r = Wordnik()

#function for jumbling words
def word_jumble(word):
  chars = random.sample(word, len(word))
  anagram = ''.join(chars)
  return anagram

#initialize client
intents = discord.Intents.default()
intents.message_content = True

#initialize bot commands
bot = commands.Bot(command_prefix='!', intents=intents)

#command for handling anagram game
@bot.command(name="anagram")
async def anagram_start(ctx):
  
  #define global variables
  global anagram_game_started, anagram_normal, anagram_jumbled, anagram_game_finished

  #makes sure a game is not in progress
  if anagram_game_started:
    await ctx.send("Game in progress!")
    return
  
  #gets the anagram word and normal word
  valid_word = False
  while not valid_word:
    word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount=15, minLength=4)
    if word:
      valid_word = True
  anagram = word_jumble(word)
  anagram_normal = word.strip()
  anagram_jumbled = anagram

  #start a timer for joining the game
  timerVal = 10
  start_message = await ctx.send(f"Anagram game starting in {timerVal}s.\nReact to join!")
  await start_message.add_reaction("🎟")

  while True:
    timerVal -= 1
    await start_message.edit(content=f"Anagram game starting in {timerVal}s.\nReact to join!")
    if timerVal == 0:
      players_message = await ctx.fetch_message(start_message.id)
      for reaction in players_message.reactions:
          async for user in reaction.users():
            if user != bot.user:
              anagram_players.append(user)
      print(anagram_players)
      break
    await asyncio.sleep(1)

  #start the anagram functionality
  if len(anagram_players) == 0:
    await ctx.send("No one joined!")
  else:
    await ctx.send("Your word is: " + anagram)
    anagram_game_started = True
    timerVal = 60
    #message = await ctx.send(f"Timer: {timerVal}")
    while True:
      timerVal -= 1
      if timerVal == 0:
        #await message.edit(content=f"Times up!")
        break
      #await message.edit(content=f"Timer: {timerVal}")
      await asyncio.sleep(1)
    
    if not anagram_game_finished:
      await ctx.send(f"No one got it! The word was {anagram_normal}")
      anagram_game_started = False
      anagram_normal = ""
      anagram_jumbled = ""
    else:
      anagram_game_finished = False


async def timer(ctx, time):
  timerVal = int(time)
  #message = await ctx.send(f"Timer: {timerVal}")
  while True:
    timerVal -= 1
    if timerVal == 0:
      #await message.edit(content=f"Times up!")
      break
    #await message.edit(content=f"Timer: {timerVal}")
    await asyncio.sleep(1)


#parses sent messages
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  await bot.process_commands(message)
  global anagram_game_started, anagram_normal, anagram_jumbled, anagram_game_finished, anagram_players
  if anagram_game_started and message.author in anagram_players:
    print(message.content + " vs " + anagram_normal)
    if message.content.lower() == anagram_normal:
      await message.reply(f"You did it! The word was {anagram_normal}")
      anagram_game_started = False
      anagram_game_finished = True
      anagram_normal = ""
      anagram_jumbled = ""
      anagram_players = []



bot.run(token['token'])