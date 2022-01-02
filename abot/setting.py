import discord
from discord.ext import commands
import psycopg2
from config import db_login, db_host, db_name, db_password

class Setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = psycopg2.connect(dbname=db_name, user=db_login,
                            password=db_password, host=db_host )
        sql = db.cursor()
        server = guild.id
        sql.execute(
            """CREATE TABLE IF NOT EXISTS "%s" (id TEXT, bio TEXT, voice_name TEXT, vcid TEXT, catid TEXT, money BIGINT);""",
            (server,))
        db.commit()
        sql.close()
        db.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild.id
        member_id = member.id
        db = psycopg2.connect(dbname=db_name, user=db_login,
                            password=db_password, host=db_host )
        sql = db.cursor()
        sql.execute("""SELECT EXISTS(SELECT id FROM "%s" WHERE id = %s);""", (str(member_id),))
        req = sql.fetchone()
        req1 = " ".join(str(x) for x in req)
        if req1 == "False":
            sql.execute("""INSERT INTO "%s" (id, money) VALUES (%s, 0);""", (server, str(member_id),))
            db.commit()
        sql.close()
        db.close()

def setup(bot):
    bot.add_cog(Setting(bot))