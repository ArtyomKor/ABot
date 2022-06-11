# временно не работает из-за отсутствия ContextMenu в когах

import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect('db/abot.db')
        self.sql = self.db.cursor()
        print("user.py connected!")

    @commands.command()
    async def user(self, ctx, message: discord.Message):
        match message.author.status:
            case discord.Status.online: status = "<:online:979549939573088286> В сети"
            case discord.Status.offline: status = "<:offline:979549976797511680> Не в сети"
            case discord.Status.idle: status = "<:idle:979549885969883226> Неактивен"
            case discord.Status.dnd: status = "<:dnd:979549808631107664> Не беспокоить"

        if message.author.display_name != message.author.name:
            name=f'{message.author} ({message.author.display_name})'
        else:
            name=message.author

        try:
            bio=self.sql.execute(f"""SELECT bio FROM "{ctx.guild.id}" WHERE user_id = ?""", (message.author.id, )).fetchone()[0]
        except TypeError:
            self.sql.execute(f"""INSERT INTO "{ctx.guild.id}"(user_id) VALUES(?)""", (message.author.id, ))
            bio=self.sql.execute(f"""SELECT bio FROM "{ctx.guild.id}" WHERE user_id = ?""", (message.author.id, )).fetchone()[0]
            self.db.commit()

        desc = f"""
{bio}

**Основная информация**
**Имя пользователя**: {name}
**Статус:** {status}"""

        try:
            for i in range(3):
                if isinstance(message.author.activities[i], discord.activity.CustomActivity) and isinstance(message.author.activities[i].emoji, discord.partial_emoji.PartialEmoji):
                    desc = desc+f"\n**Пользовательский статус:** {message.author.activities[i].emoji.name} {message.author.activities[i].name}"
                elif isinstance(message.author.activities[i], discord.activity.CustomActivity):
                    desc = desc+f"\n**Пользовательский статус:** {message.author.activities[i].name}"
                if isinstance(message.author.activities[i], discord.activity.Spotify):
                    desc=desc+f"\n**Слушает:** <:Spotify:979550043176583188> {message.author.activities[i].artist} — {message.author.activities[i].title}"
                if isinstance(message.author.activities[i], discord.activity.Activity):
                    desc=desc+f"\n**Играет в:** {message.author.activities[i].name}"
        except: pass

        desc=desc+f"""
**Присоединился:** <t:{int(message.author.joined_at.timestamp())}:D> (<t:{int(message.author.joined_at.timestamp())}:R>)
**Дата регистрации:**  <t:{int(message.author.created_at.timestamp())}:D> (<t:{int(message.author.created_at.timestamp())}:R>)"""

        user_info = discord.Embed(description=desc)

        user_info.set_thumbnail(url=message.author.display_avatar.url)
        user_info.set_author(icon_url=message.author.display_avatar.url, name=f'Информация о {message.author.display_name}')
        user_info.set_footer(text=f"ID: {message.author.id}")
        await ctx.respond(embed=user_info, ephemeral=True)

    @slash_command(name='bio', description="Установка биографии(отображается в User)")
    async def bio(self, ctx, bio: discord.Option(str, "Текст биографии")):
        try:
            bio_bd=self.sql.execute(f"""SELECT bio FROM "{ctx.guild.id}" WHERE user_id = ?""", (ctx.author.id, )).fetchone()
            if isinstance(bio_bd, tuple):
                self.sql.execute(f"""UPDATE "{ctx.guild.id}" SET bio = ? WHERE user_id = ?""", (bio, ctx.author.id, ))
            else:
                self.sql.execute(f"""INSERT INTO "{ctx.guild.id}"(user_id, bio) VALUES(?, ?)""", (ctx.author.id, bio))
            self.db.commit()
            await ctx.respond(f"Успешно! Вы можете посмотреть свою биографию в User", ephemeral=True)
        except Exception as error:
            await ctx.respond(content="Странно! Что-то пошло не так и настройки не могут быть применены! Мы уже разбираемся с этим...", ephemeral=True)
            self.sql.execute('INSERT INTO bugs VALUES (?, ?, ?)', (ctx.guild.id, str(error), "bio"))
            self.db.commit()

def setup(client):
    print("Connect user.py")
    client.add_cog(User(client))