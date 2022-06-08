import discord
from discord.ext import commands
from discord.commands import slash_command
import sqlite3

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("db/abot.db")
        self.sql = self.db.cursor()
        print("settings.py connected!")

    @slash_command(description="Настроить бота")
    async def settings(self, ctx: discord.commands.context.ApplicationContext, voice: discord.Option(discord.VoiceChannel, "Голосовой канал для создания другого голосового канала")):
        try:
            voice_channel_bd=self.sql.execute(f"""SELECT * FROM settings WHERE guild = ?""", (ctx.guild.id, )).fetchone()
            if isinstance(voice_channel_bd, tuple):
                self.sql.execute(f"""UPDATE settings SET create_voice = ? WHERE guild = ?""", (voice.id, ctx.guild.id, ))
                await ctx.respond("Ваши настройки успешно обновлены!", ephemeral=True)
            else:
                self.sql.execute(f"""INSERT INTO settings VALUES(?, ?)""", (ctx.guild.id, voice.id))
                await ctx.respond("Ваши настройки успешно установлены!", ephemeral=True)
        except:
            await ctx.respond("Странно! Что-то пошло не так, мы уже с этим разбираемся...", ephemeral=True)

def setup(client):
    print("Connect settings.py")
    client.add_cog(Settings(client))