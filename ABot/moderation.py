import discord
from discord.ext import commands
from discord.commands import slash_command
import re
import datetime

def check_permission(member: discord.Member):
    if member.top_role.permissions.administrator == True: return True
    else: return False

class BanButton(discord.ui.Button):
    def __init__(self, interacted: discord.Member, user: discord.Member):
        self.user = user
        self.interacted = interacted
        super().__init__(style = discord.ButtonStyle.red, label='Забанить', disabled=check_permission(user))

    async def callback(self, interaction: discord.Interaction):
        if self.interacted.id == interaction.user.id:
            await self.user.ban(reason=f"Был забанен {interaction.user}")
            ban_embed = discord.Embed(title=f"{self.user} был забанен!")
            await interaction.message.edit(embed=ban_embed, delete_after=10.0)
            await interaction.response.send_message(f"{self.user} был забанен!", ephemeral=True)

class KickButton(discord.ui.Button):
    def __init__(self, interacted: discord.Member, user: discord.Member):
        self.user = user
        self.interacted = interacted
        super().__init__(style = discord.ButtonStyle.secondary, label='Кикнуть', disabled=check_permission(user))

    async def callback(self, interaction: discord.Interaction):
        if self.interacted.id == interaction.user.id:
            await self.user.kick(reason=f"Был кикнут {interaction.user}`ом")
            kick_embed = discord.Embed(title=f"{self.user} был кикнут!")
            await interaction.message.edit(embed=kick_embed, delete_after=10.0)
            await interaction.response.send_message(f"{self.user} был кикнут!", ephemeral=True)

class MuteButton(discord.ui.Button):
    def __init__(self, interacted: discord.Member, user: discord.Member):
        self.user = user
        self.interacted = interacted
        super().__init__(style = discord.ButtonStyle.secondary, label='Замутить', disabled=check_permission(user))

    async def callback(self, interaction: discord.Interaction):
        if self.interacted.id == interaction.user.id:
            mute_embed = discord.Embed(title=f"Выберите время")
            view = discord.ui.View(timeout=None)
            view.add_item(MuteSelect(self.interacted, self.user))
            await interaction.message.edit(embed=mute_embed, view=view)
            await interaction.response.send_message(f"Выбирайте время мута.", ephemeral=True)

class MuteSelect(discord.ui.Select):
    def __init__(self, interacted: discord.Member, user: discord.Member):
        self.interacted = interacted
        self.user = user
        super().__init__(placeholder="Время мута", disabled=check_permission(user))
        self.add_option(label="1 минута", value=f"1m")
        self.add_option(label="5 минут", value=f"5m")
        self.add_option(label="10 минут", value=f"10m")
        self.add_option(label="1 час", value=f"1h")
        self.add_option(label="1 день", value=f"1d")
        self.add_option(label="1 неделя", value=f"1w")
        self.add_option(label="2 недели", value=f"2w")
        self.add_option(label="3 недели", value=f"3w")
        self.add_option(label="1 месяц", value=f"1mon")

    async def callback(self, interaction: discord.Interaction):
        if self.interacted.id == interaction.user.id:
            time = re.sub("[0-9]", "", self.values[0])
            minutes = 0
            hours = 0
            days = 0
            weeks = 0
            seconds = 0
            num = int("".join(c for c in self.values[0] if  c.isdecimal()))
            if time == "m":
                minutes = num
            elif time == "h":
                hours = num
            elif time == "d":
                days = num
            elif time == "w":
                weeks = num
            elif time == "mon":
                days = 27
                hours = 23
                minutes = 59
                seconds = 59
            await self.user.timeout_for(duration=datetime.timedelta(seconds=float(seconds), days=float(days), minutes=float(minutes), hours=float(hours), weeks=float(weeks)), reason=f"{self.user} был замучен на {self.values[0]}")
            embed = discord.Embed(title=f"{self.user} был замучен!")
            await interaction.message.edit(embed=embed, view=None, delete_after=10.0)
            await interaction.response.send_message(f"{self.user} был замучен!", ephemeral=True)

class UnMuteButton(discord.ui.Button):
    def __init__(self, interacted: discord.Member, user: discord.Member):
        self.user = user
        self.interacted = interacted
        super().__init__(style = discord.ButtonStyle.secondary, label='Размутить', disabled=check_permission(user))

    async def callback(self, interaction: discord.Interaction):
        if self.interacted.id == interaction.user.id:
            await self.user.remove_timeout(reason=f"Был размучен {interaction.user}`ом")
            unmute_embed = discord.Embed(title=f"{self.user} был размучен!")
            await interaction.message.edit(embed=unmute_embed, view=None, delete_after=10.0)
            await interaction.response.send_message(f"{self.user} был размучен!", ephemeral=True)

class CloseButton(discord.ui.Button):
    def __init__(self, interacted: discord.Member, user: discord.Member):
        self.user = user
        self.interacted = interacted
        super().__init__(style = discord.ButtonStyle.secondary, label='Закрыть', disabled=check_permission(user))

    async def callback(self, interaction: discord.Interaction):
        if self.interacted.id == interaction.user.id:
            await interaction.message.delete()

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("moderation.py connected!")

    @slash_command(name='admin', description='Админ панель')
    async def admin(self, ctx: discord.ApplicationContext, user: discord.Option(discord.Member, "Пользователь")):
        embed = discord.Embed(title=user)
        view = discord.ui.View(timeout=None)
        view.add_item(BanButton(ctx.author, user))
        view.add_item(KickButton(ctx.author, user))
        if user.timed_out == False:
            view.add_item(MuteButton(ctx.author, user))
        else:
            view.add_item(UnMuteButton(ctx.author, user))
        view.add_item(CloseButton(ctx.author, user))
        await ctx.respond(embed=embed, view=view)

def setup(client):
    print("Connect moderation.py")
    client.add_cog(Moderation(client))