import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from ABot.cache import VoiceCache

class Channels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voices = VoiceCache()
        self.db = sqlite3.connect("db/abot.db")
        self.sql = self.db.cursor()
        print("channels.py connected!")

    @commands.Cog.listener()
    async def on_ready(self):
        self.sql.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.sql.fetchall()
        for guild in tables:
            if guild[0] != "bugs" and guild[0] != "settings":
                voices = self.sql.execute(f"""SELECT * FROM "{guild[0]}";""").fetchall()
                for voice in voices:
                    await self.voices.append_channel_name(author=voice[0], name=voice[2], guild=guild[0])

    @commands.hybrid_command(description="Очистить канал на определённое количество сообщений")
    @app_commands.describe(count="Количество сообщений для удаления.")
    async def clear(self, interaction: commands.Context, count: int):
        deleted = await interaction.channel.purge(limit=count)
        await interaction.send(f'Удалено {len(deleted)} сообщений(ия, ие)!', ephemeral=True)
    
    @commands.hybrid_command(description="Установить имя для своего голосового канала")
    @app_commands.describe(name="Имя для голосового канала.")
    async def name(self, interaction: commands.Context, name: str):
        if interaction.author.voice != None:
            if (interaction.author.id, interaction.author.voice.channel.id) in self.voices.channels.items():
                await interaction.author.voice.channel.edit(name=name)
            else:
                await interaction.send("Этот канал принадлежит не Вам!", ephemeral=True)
        self.sql.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.sql.fetchall()
        for guild in tables:
            if guild[0] != "bugs" and guild[0] != "settings":
                if guild[0] == f"{interaction.guild.id}":
                    name_bd=self.sql.execute(f"""SELECT * FROM "{guild[0]}" WHERE user_id = ?""", (interaction.author.id, )).fetchone()
                    if isinstance(name_bd, tuple):
                        self.sql.execute(f"""UPDATE "{guild[0]}" SET voice = ? WHERE user_id = ?""", (name, interaction.author.id, ))
                        await interaction.send("Ваше название успешно обновлено!", ephemeral=True)
                    else:
                        self.sql.execute(f"""INSERT INTO "{guild[0]}"(user_id, voice) VALUES(?, ?)""", (interaction.author.id, name))
                        await interaction.send("Ваше название успешно установлено!", ephemeral=True)
                    await self.voices.append_channel_name(author=interaction.author.id, name=name, guild=str(interaction.guild.id))
                    self.db.commit()        

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        if after.channel != None and member in after.channel.members and after.channel.id == self.sql.execute("""SELECT create_voice FROM settings WHERE guild = ?""", (after.channel.guild.id, )).fetchone()[0]:
            overwrites = {
                member: discord.PermissionOverwrite(manage_channels=True, manage_permissions=True)
            }
            if self.voices.channels_name[f"{after.channel.guild.id}:{member.id}"] == None:
                name = f"Канал {member.name}"
            else:
                name = self.voices.channels_name[f"{after.channel.guild.id}:{member.id}"]
            channel = await after.channel.category.create_voice_channel(name=name, reason=f"Создание голосового канала из {after.channel.name} пользователем {member}", overwrites=overwrites)
            await member.move_to(channel, reason=f"Создание голосового канала из {after.channel.name} пользователем {member}")
            await self.voices.append_channel(member.id, channel.id)
        if before.channel != None and before.channel.id in self.voices.channels.values() and len(before.channel.members) == 0:
            await before.channel.delete()
            await self.voices.pop_channel(before.channel.id)

async def setup(client):
    print("Connect channels.py")
    await client.add_cog(Channels(client))