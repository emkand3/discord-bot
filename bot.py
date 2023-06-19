import discord
from discord.ext import commands
from random_word import Wordnik
import random
import json

anagram_game_started = False
anagram_game_finished = False
anagram_jumbled = ""
anagram_normal = ""

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
  
  global anagram_game_started, anagram_normal, anagram_jumbled, anagram_game_finished

  if anagram_game_started:
    print("no no")
    await ctx.send("Game in progress!")
    return
  print("command received")
  valid_word = False
  while not valid_word:
    word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount=15, minLength=4)
    print(word)
    if word:
      valid_word = True
  anagram = word_jumble(word)
  anagram_normal = word.strip()
  anagram_jumbled = anagram
  print(anagram)
  await ctx.send("Starting your anagram game...")
  #TODO: add functionality for specific users joining a game
  await ctx.send("Your word is: " + anagram)
  anagram_game_started = True

#parses sent messages
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  await bot.process_commands(message)
  global anagram_game_started, anagram_normal, anagram_jumbled, anagram_game_finished
  if anagram_game_started:
    print(message.content + " vs " + anagram_normal)
    if message.content == anagram_normal:
      print("yassss done")
      anagram_game_started = False
      anagram_game_finished = True
      await message.reply("yass you did it")


bot.run(token['token'])