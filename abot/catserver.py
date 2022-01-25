import discord
from discord.ext import commands

class Catserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        role_id = 932546817613262918
        guild = await self.bot.fetch_guild(payload.guild_id)
        role = guild.get_role(int(role_id))
        if payload.message_id == 932536431463792690:
            if not role in payload.member.roles:
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        role_id = 932546817613262918
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(int(role_id))
        member = guild.get_member(payload.user_id)
        if payload.message_id == 932536431463792690:
            if role in member.roles:
                await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Catserver(bot))
