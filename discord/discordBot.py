import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)
# bot = discord.Client(intents=discord.Intents.default())

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
    """Adds two numbers together."""
    await ctx.send("dziala")

@bot.command()
async def get_channel(ctx):
    channel = discord.utils.get(ctx.guild.channels, name="wycinki-i-ciekawostki")
    await channel.send("dziala")


bot.run(DISCORD_TOKEN)
