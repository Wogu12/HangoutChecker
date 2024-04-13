import sys
import discord
import os
import json
from discord.ext import commands
from dotenv import load_dotenv
from gSheetManipulate import SpreadsheetManipulation


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))

intents = discord.Intents.all()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    #channel = discord.utils.get(ctx.guild.channels, name=given_name)
    channel = bot.get_channel(CHANNEL)
    # channel = discord.utils.get(guild.channels, name="BestChannel")
    await channel.send("test")
    
@bot.listen('on_message')
async def hello(message):
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.channel.send("hey dirtbag")


@bot.command()
async def test(ctx):
    await ctx.send("dziala")

@bot.command()
async def get_channel(ctx):
    print('trying...')
    channel = discord.utils.get(ctx.guild.channels, name="wycinki-i-ciekawostki")
    searcher = SpreadsheetManipulation()

    results = searcher.check_tomorrow()
    for days in results:
        result_string = '\n'.join(results)
    print('end?')
    await channel.send(result_string)


bot.run(DISCORD_TOKEN)
