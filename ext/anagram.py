import discord
from discord.ext import commands
import asyncio, random
from random_word import Wordnik

#   global constants for game state (possibly make configurable?)
JOIN_TIME = 20
GAME_TIME = 60

#global variable for loading in Wordnik object
r = Wordnik()

#helper function for scrambling letters for words
def word_jumble(word):
  chars = random.sample(word, len(word))
  anagram = ''.join(chars)
  return anagram

###     ANAGRAM COG       ###
#   self.active_guild is a dictionary of dictionaries to keep track
#   of game states per guild

class Anagram(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_guilds = {}
    
    #   anagram command ($anagram)
    @commands.command(name='anagram')
    async def game_initializer(self, ctx):

        #checks if a guild has a game in progess
        if ctx.guild.id in self.active_guilds:
            await ctx.send("Game in progress!")
            return
        
        #create a dictionary for variables per guild and sets variables
        self.active_guilds[ctx.guild.id] = {
            "start": False,
            "word": "",
            "jumble": "",
            "players": [],
            "over": False
        }
        self.active_guilds[ctx.guild.id]["start"] = True

        #gets the anagram word and normal word and sets those per guild
        valid_word = False
        while not valid_word:
            word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount=15, minLength=4)
            if word:
                valid_word = True
        self.active_guilds[ctx.guild.id]["jumble"] = word_jumble(word)
        self.active_guilds[ctx.guild.id]["word"] = word.strip()

        #start a timer for joining the game
        joinTimerVal = JOIN_TIME
        start_message = await ctx.send(f"Anagram game starting in {joinTimerVal}s.\nReact to join!")
        await start_message.add_reaction("🎟")

        #gather players for game
        while True:
            joinTimerVal -= 1
            await start_message.edit(content=f"Anagram game starting in {joinTimerVal}s.\nReact to join!")
            if joinTimerVal == 0:
                players_message = await ctx.fetch_message(start_message.id)
                for reaction in players_message.reactions:
                    async for user in reaction.users():
                        if user != self.bot.user:
                            self.active_guilds[ctx.guild.id]["players"].append(user)
                break
            await asyncio.sleep(1)

        #start the anagram functionality
        if len(self.active_guilds[ctx.guild.id]["players"]) == 0:
            await ctx.send("No one joined!")
            del self.active_guilds[ctx.guild.id]
            return
        else:
            await ctx.send(f"Your word is: {self.active_guilds[ctx.guild.id]['jumble']}")
            gameTimerVal = GAME_TIME
            while True:
                gameTimerVal -= 1
                if gameTimerVal == 0:
                    break
                if self.active_guilds[ctx.guild.id]["over"]:
                    break
                await asyncio.sleep(1)
            #handles state where word is not guessed in time
            if ctx.guild.id in self.active_guilds and not self.active_guilds[ctx.guild.id]["over"]:
                await ctx.send(f"No one got it! The word was {self.active_guilds[ctx.guild.id]['word']}")
                del self.active_guilds[ctx.guild.id]
            if ctx.guild.id in self.active_guilds and self.active_guilds[ctx.guild.id]["over"]:
                del self.active_guilds[ctx.guild.id]
    
    #   listens for messages from user
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        #listens specifically for anagram game messages by making sure the messager is registered in the game
        if message.guild.id in self.active_guilds and message.author in self.active_guilds[message.guild.id]["players"]:
            if message.content.lower() == self.active_guilds[message.guild.id]["word"]:
                await message.reply(f"You did it! The word was {self.active_guilds[message.guild.id]['word']}")
                self.active_guilds[message.guild.id]["over"] = True

async def setup(bot: commands.Bot):
    await bot.add_cog(Anagram(bot))