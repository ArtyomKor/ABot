config = open("config.ini", "r", encoding="utf-8")

TOKEN = config.readlines[0]

import discord

client = discord.Bot(intents=discord.Intents.all())


client.load_extension("ABot.user")
client.load_extension("ABot.server")
client.load_extension("ABot.events")
client.load_extension("ABot.channels")
client.load_extension("ABot.moderation")
client.load_extension("ABot.settings")


client.run(TOKEN)