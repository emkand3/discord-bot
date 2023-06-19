import discord
from random_word import Wordnik
import random
import json

file = open('config.json')
token = json.load(file)

r = Wordnik()

def word_jumble(word):
  chars = random.sample(word, len(word))
  anagram = ''.join(chars)
  return anagram

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

# Return a single random word
  if message.content.startswith('$a'):
    valid_word = False
    while not valid_word:
      word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount=15, minLength=4)
      if word:
        valid_word = True
    anagram = word_jumble(word)
    print(anagram + " ...actual word: " + word)
    await message.channel.send(anagram + " ...actual word: " + word)

client.run(token['token'])