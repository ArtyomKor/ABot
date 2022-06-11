config = open("config.ini", "r", encoding="utf-8")

TOKEN = config.readlines()[0]

import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix="ABot.", intents=discord.Intents.all())


async def load(bot: commands.Bot):

    # await bot.load_extension("ABot.user")
    await bot.load_extension("ABot.server")
    await bot.load_extension("ABot.events")
    await bot.load_extension("ABot.channels")
    await bot.load_extension("ABot.moderation")
    await bot.load_extension("ABot.settings")

asyncio.run(load(client))
client.run(TOKEN)
