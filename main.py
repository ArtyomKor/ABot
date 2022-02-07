from config import token
import discord
from discord.ext import commands

bot = discord.Bot(intents=discord.Intents.all())

bot.load_extension("abot.setting")
bot.load_extension("abot.otchet")
bot.load_extension("abot.fun")
bot.load_extension("abot.info")
bot.load_extension("abot.voice")
bot.load_extension("abot.moderation")
bot.load_extension("abot.automoder")

@bot.event
async def on_ready():
    print('Bot connected to application!')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("ABoBot"))

bot.run(token)

