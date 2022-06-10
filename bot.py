config = open("config.ini", "r", encoding="utf-8")

TOKEN = config.readlines()[0]

import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix="ABot.", intents=discord.Intents.all())

async def load(client: commands.Bot):

    #await client.load_extension("ABot.user")
    await client.load_extension("ABot.server")
    await client.load_extension("ABot.events")
    await client.load_extension("ABot.channels")
    await client.load_extension("ABot.moderation")
    await client.load_extension("ABot.settings")

asyncio.run(load(client))
client.run(TOKEN)