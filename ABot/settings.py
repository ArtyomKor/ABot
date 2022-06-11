import discord
from discord.ext import commands
from discord import app_commands
import sqlite3


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("db/abot.db")
        self.sql = self.db.cursor()
        print("settings.py connected!")

    @commands.hybrid_command(description="Настроить бота")
    @app_commands.describe(voice='Голосовой канал для создания другого голосового канала')
    async def settings(self, interaction: commands.Context, voice: discord.VoiceChannel):
        try:
            voice_channel_bd = self.sql.execute(f"""SELECT * FROM settings WHERE guild = ?""",
                                                (interaction.guild.id,)).fetchone()
            if isinstance(voice_channel_bd, tuple):
                self.sql.execute(f"""UPDATE settings SET create_voice = ? WHERE guild = ?""",
                                 (voice.id, interaction.guild.id,))
                await interaction.send("Ваши настройки успешно обновлены!", ephemeral=True)
            else:
                self.sql.execute(f"""INSERT INTO settings VALUES(?, ?)""", (interaction.guild.id, voice.id))
                await interaction.send("Ваши настройки успешно установлены!", ephemeral=True)
        except Exception as error:
            print(error)
            await interaction.send("Странно! Что-то пошло не так, мы уже с этим разбираемся...", ephemeral=True)


async def setup(client):
    print("Connect settings.py")
    await client.add_cog(Settings(client))
