import discord
from discord.ext import commands
from discord.commands import Option
import psycopg2
import platform
import psutil
from config import db_login, db_host, db_name, db_password

voices = []

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global channel
        db = psycopg2.connect(dbname=db_name, user=db_login,
                            password=db_password, host=db_host )
        sql = db.cursor()
        server_id = member.guild.id
        member_id = member.id
        guild = member.guild
        sql.execute("""SELECT vcid FROM "%s" WHERE id = %s; """, (server_id, str(server_id)))
        create_id=sql.fetchone()
        createId = " ".join(str(x) for x in create_id)
        create = discord.utils.get(guild.voice_channels, id=int(createId))
        if before.channel is None and after.channel is create:
            sql.execute("""SELECT voice_name FROM "%s" WHERE id = %s;""", (server_id, str(member_id),))
            name = sql.fetchone()
            sql.execute("""SELECT catid FROM "%s" WHERE id = %s;""", (server_id, str(server_id)))
            catId =sql.fetchone()
            cat_Id = " ".join(str(x) for x in catId)
            print(cat_Id)
            if name is None:
                name_channel = f'Голосовой канал {member}'
            else:
                name_channel = " ".join(str(x) for x in name)
            category = discord.utils.get(guild.categories, id=int(cat_Id))
            channel = await guild.create_voice_channel(name_channel, category=category)
            await member.move_to(channel)
            voices.append(channel)
        if before.channel is not None and after.channel is None or after.channel is not None:
            for i in voices:
                if before.channel is i and after.channel is None or not None:
                    if len(before.channel.members) == 0:
                        await before.channel.delete()
                        vindex = voices.index(i)
                        voices.pop(vindex)

    @commands.slash_command(name='name', description='Установка имени голосового канала.')
    async def name(self, ctx, имя: Option(str, 'Новое имя канала.', required=True)):
        name = имя
        try:
            db = psycopg2.connect(dbname=db_name, user=db_login,
                            password=db_password, host=db_host )
            sql = db.cursor()
            server = ctx.guild.id
            member_id = ctx.author.id
            sql.execute("""SELECT EXISTS(SELECT voice_name FROM "%s" WHERE id = %s);""", (server, str(member_id),))
            req = sql.fetchone()
            if req == "(False,)":
                sql.execute("""INSERT INTO "%s" (id, voice_name) VALUES (%s, %s);""", (server, str(member_id), name,))
                db.commit()
            else:
                sql.execute("""UPDATE "%s" SET voice_name = %s WHERE id = %s;""", (server, str(name), str(member_id)))
                db.commit()
            sql.close()
            db.close()
            channel = ctx.author.voice.channel
            await channel.edit(name=name)
            await ctx.respond('Успешно!')
        except Exception as error:
            await ctx.respond(
                "Вы не находитесь в голосовом канале!")

    @commands.slash_command(name='limit', description='Установка лимита в голосовом канале.')
    async def limit(self, ctx, лимит: Option(int, 'Количество максимальных пользователей. 0 - бесконечно.', required=False,
                                    default=0)):
        limit = лимит
        try:
            channel = ctx.author.voice.channel
            await channel.edit(user_limit=limit)
            await ctx.respond('Успешно!')
        except:
            if limit >= 100:
                await ctx.respond('Максимальный лимит 99!')
            elif limit <= 99:
                await ctx.respond("Вы не находитесь в голосовом канале!")

    @commands.slash_command(name='idvoice', description='Установить id голосовго канала для создания другого голосового канала.')
    @commands.has_permissions(administrator=True)
    async def vccreate(self, ctx, канал: Option(discord.VoiceChannel, 'id канала', required=True), категория: Option(discord.CategoryChannel, 'id категории', required=True)):
        id = канал.id
        catid = категория.id
        server=ctx.guild.id
        db = psycopg2.connect(dbname=db_name, user=db_login,
                            password=db_password, host=db_host )
        sql = db.cursor()
        sql.execute("""SELECT EXISTS(SELECT vcid FROM "%s");""", (server,))
        req = sql.fetchone()
        print(req)
        try:
            sql.execute("""INSERT INTO "%s" (id, vcid, catid) VALUES (%s, %s, %s);""", (server, str(server), str(id), str(catid),))
            db.commit()
            await ctx.respond('Успешно!')
        except:
            await ctx.respond('Ошибка.')

    @commands.slash_command(name='status', description='Узнать состояние сервера.')
    async def status(self, ctx):
        cpu = psutil.cpu_percent(interval=None)
        emb = discord.Embed(title="Статус ABot", colour=discord.Color.purple())
        emb.add_field(name='Версия Python', value=platform.python_version())
        emb.add_field(name='Версия pycord', value=discord.__version__)
        emb.add_field(name='Информация о сервере', value=f'Загрузка ЦП: `{cpu}%`\n'
                                                        f'RAM: `{psutil.virtual_memory().used // 1024 // 1024} МБ`/`{psutil.virtual_memory().total // 1024 // 1024} МБ`\n')
        emb.add_field(name='Временных каналов', value=f'{len(voices)}')
        await ctx.respond(embed=emb)

def setup(bot):
    bot.add_cog(Voice(bot))