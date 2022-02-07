import discord
from discord.ext import commands
import psycopg2
from datetime import timedelta
from config import *

async def checkmute(message):
    if len(message) >= 7:
        p = 0
        for i in range(len(message.content)):
            if message.content[i] == message.content.upper()[i]:
                p += 1
        if int(p/len(message.content)*100) >= 40: return True

    else: return False

db = psycopg2.connect(dbname=db_name, user=db_login,
                            password=db_password, host=db_host)
sql = db.cursor()

class AutoModer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		
    @commands.Cog.listener()
    async def on_message(self, message):
        orig_message = message.content
        message = ''.join(char for char in str(orig_message) if char.isalnum())
        sql.execute("""SELECT moder_id FROM "settings" WHERE server_id = %s;""", [message.guild.id])
        moderid = sql.fetchone()
        moder_id = " ".join(str(x) for x in moderid)
        moder_role = message.guild.get_role(int(moder_id))
        if await checkmute(message.content):
            await message.author.timeout_for(timedelta(minutes=5), reason="Авто-модерация")

def setup(bot):
    bot.add_cog(AutoModer(bot))