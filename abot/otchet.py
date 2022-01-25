import discord
from discord.ext import commands
from discord.commands import Option

class Otchet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[923482206888947713],name='стол')
    @commands.has_role(923805234298494986)
    async def стол(self, ctx, заявка: Option(str, 'П-платники Б-бесплатники', required=True)):
        if ctx.channel.id == 924596701703061504:
            global plbesp
            plbesp = заявка
            await ctx.respond('Успешно.')
        else:
            await ctx.send("Вы не в том канале!")


    @commands.slash_command(guild_ids=[923482206888947713],name='деж')
    @commands.has_role(923805234298494986)
    async def деж(self, ctx, назначены: Option(str, 'Фамилии назначенных.', required=True)):
        dezh = назначены
        if ctx.channel.id == 924596701703061504:
            global dezhur
            dezhur = dezh
            await ctx.respond('Успешно.')
        else:
            await ctx.send("Вы не в том канале!")


    @commands.slash_command(guild_ids=[923482206888947713],name='отс')
    @commands.has_role(923805234298494986)
    async def отс(self, ctx, отсутствуют: Option(str, 'Фамилии отсутствующих.', required=True)):
        ots = отсутствуют
        if ctx.channel.id == 924596701703061504:
            global otst
            otst = ots
            await ctx.respond('Успешно.')
        else:
            await ctx.respond("Вы не в том канале!")


    @commands.slash_command(guild_ids=[923482206888947713],name='отчёт')
    @commands.has_role(923805234298494986)
    async def отчёт(self, ctx):
        if ctx.channel.id == 924596701703061504:
            await ctx.respond("Начинаю обработку...")
            embed = discord.Embed(
                title="Отчёт",
                colour=discord.Color.green())
            embed.add_field(name="Назначены дежурными:", value=dezhur, inline=True)
            embed.add_field(name="Заявка: ", value=plbesp, inline=True)
            embed.add_field(name="Отсутствуют:", value=otst, inline=True)
            chan = discord.utils.get(ctx.guild.channels, id=923807471708028948)
            otchet = await chan.send(embed=embed)
            await otchet.add_reaction('✅')
            global otch_id
            otch_id = otchet.id

        else:
            await ctx.respond("Вы не в том канале!")

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == otch_id and payload.member != "ABot#3808":
            chat = discord.utils.get(self.bot.get_all_channels(), id=924596701703061504)
            await chat.send('Ваш отчёт просмотрен!')
            print(payload.member)

def setup(bot):
    bot.add_cog(Otchet(bot))
