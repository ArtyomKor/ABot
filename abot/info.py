import discord
from discord.ext import commands
from discord.commands import Option
import psycopg2

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='user', description='Вывести информацию о пользователе.')
    async def user(self, ctx, пользователь: Option(discord.Member, 'Пользователь', required=False, default=None)):
        db = psycopg2.connect(dbname='bot', user='postgres',
                            password='pgdb270708wW@', host='45.90.217.187' )
        sql = db.cursor()
        if пользователь is None:
            пользователь = await ctx.guild.fetch_member(ctx.author.id)
        author = пользователь.id
        command = """SELECT bio FROM "%s" WHERE id = %s;"""
        server = ctx.guild.id
        sql.execute(command, (server, str(author),))
        desc = sql.fetchone()
        if desc == None:
            descr = 'Тут ничего нет! Но вы можете установить свой текст с помощью /bio'
        else:
            descr = " ".join(str(x) for x in desc)
        status = {
            discord.Status.online: "Онлайн",
            discord.Status.idle: "Отошел",
            discord.Status.dnd: "Не беспокоить",
            discord.Status.offline: "Не в сети",
        }
        embed = discord.Embed(
            title=f"Информация о {пользователь.display_name}",
            description=descr,
            colour=discord.Color.purple())
        embed.set_thumbnail(url=пользователь.avatar)
        embed.set_author(name=пользователь.display_name, icon_url=пользователь.avatar)
        embed.set_footer(text=f"ID: {пользователь.id}")
        embed.add_field(name="Имя пользователя", value=пользователь.name)
        embed.add_field(name="Статус", value=status[пользователь.status], inline=False)
        embed.add_field(name="Присоединился",
                        value=f"<t:{int(пользователь.joined_at.timestamp())}:D>",
                        inline=True)
        embed.add_field(name="Создал аккаунт", value=f"<t:{int(пользователь.created_at.timestamp())}:f>", inline=True)
        await ctx.respond(embed=embed)
        sql.close()
        db.close()

    @commands.slash_command(name='bio', description='Установка биографии.')
    async def bio(self, ctx, bio: Option(str,'Ваш текст отображаемый в user',required=True)):
        db = psycopg2.connect(dbname='bot', user='postgres',
                            password='pgdb270708wW@', host='45.90.217.187' )
        sql = db.cursor()
        author = ctx.author.id
        server = ctx.guild.id
        sql.execute("""SELECT EXISTS(SELECT bio FROM "%s" WHERE id = %s);""", (server, str(author)))
        req = sql.fetchone()
        if str(req) == "(True,)":
            command = """UPDATE "%s" SET bio = %s WHERE id = %s;"""
            sql.execute(command, (server, str(bio), str(author),))
            db.commit()
            print('+')
        else:
            command = """INSERT INTO "%s" (id, bio) VALUES (%s, %s);"""
            sql.execute(command, (server, str(author), str(bio),))
            db.commit()
            print('-')
        sql.close()
        db.close()
        await ctx.respond('Успешно!')

def setup(bot):
    bot.add_cog(Info(bot))
