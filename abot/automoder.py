import discord
from discord.ext import commands
from datetime import timedelta
import re

async def checkmute(message):
    if len(message.content) >= 7:
        mess = re.sub("[0-9]", "", message.content)
        p = 0
        mess1 = ''.join(char for char in mess if char.isalnum())
        for i in range(len(mess1)):
            if mess1[i] == mess1.upper()[i]:
                p += 1
        if p == 0 or len(mess1) == 0: return False
        elif int(p/len(mess1)*100) >= 40: return True
    else: return False

class AutoModer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.owner is not message.author:
            if await checkmute(message):
                await message.author.timeout_for(timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=5, hours=0, weeks=0), reason="Авто-модерация")

def setup(bot):
    bot.add_cog(AutoModer(bot))
