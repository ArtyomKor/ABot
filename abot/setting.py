import discord
from discord.ext import commands
from discord.commands import Option
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
        sql.execute("""INSERT INTO "settings" (server_id) VALUES (%s);""", [guild.id])
        for i in guild.members:
            sql.execute("""INSERT INTO "%s"(id, money, bio, voice_name) VALUES (%s, %s, %s, %s);""", (guild.id, str(i.id), 0, "Тут ничего нет! Но вы можете добавить свой текст сюда с помощью /bio", "first setting name",))
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
        sql.execute("""SELECT EXISTS(SELECT id FROM "%s" WHERE id = %s);""", (int(member.guild.id), str(member_id),))
        req = sql.fetchone()
        req1 = " ".join(str(x) for x in req)
        if req1 == "False":
            sql.execute("""INSERT INTO "%s" (id, money, voice_name) VALUES (%s, 0, %s);""", (server, str(member_id), "first setting name",))
            db.commit()
        sql.close()
        db.close()

    @commands.slash_command(name="settings", description="Установка роли администратора.")
    @commands.has_permissions(administrator=True)
    async def setting(self, ctx, moder_role: Option(discord.Role, 'Роль модераторов.', required=True)):
        db = psycopg2.connect(dbname=db_name, user=db_login,
                            password=db_password, host=db_host )
        sql = db.cursor()
        try:
            sql.execute("""UPDATE "settings" SET moder_id = %s WHERE server_id = %s;""", [moder_role.id, ctx.guild.id,])
            db.commit()
            await ctx.respond(content="Настройки сохранены успешно!", ephemeral=True)
        except:
            await ctx.respond(content="Произошла ошибка!", ephemeral=True)
        sql.close()
        db.close()

def setup(bot):
    bot.add_cog(Setting(bot))
