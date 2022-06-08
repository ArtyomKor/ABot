import discord
from discord.ext import commands
from discord.commands import slash_command

class Server(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("server.py connected!")

    @slash_command(name='serverinfo', description='Информация о сервере')
    async def serverinfo(self, ctx):
        bot_count = 0
        human_count = 0
        online_count = 0
        idle_count = 0
        dnd_count = 0
        offline_count = 0
        for i in ctx.guild.members:
            if i.bot == True:
                bot_count=bot_count+1
            else:
                human_count=human_count+1
            match i.status:
                case discord.Status.online: online_count=online_count+1
                case discord.Status.offline: offline_count=offline_count+1
                case discord.Status.idle: idle_count=idle_count+1
                case discord.Status.dnd: dnd_count=dnd_count+1

        match ctx.guild.verification_level:
            case discord.VerificationLevel.none: verification_level = "Отсутствует"
            case discord.VerificationLevel.low: verification_level = "Низкий"
            case discord.VerificationLevel.medium: verification_level = "Средний"
            case discord.VerificationLevel.high: verification_level = "Высокий"
            case discord.VerificationLevel.highest: verification_level = "Самый высокий"

        embed = discord.Embed(title=f'Информация о сервере {ctx.guild.name}')
        embed.add_field(name='Участники:', value=f"""
<:members_total:979727117115858964> Всего: **{ctx.guild.member_count}**
<:members:979727108463022090> Людей: **{human_count}**
<:bot:979727091924869180> Ботов: **{bot_count}**""", inline=True)
        embed.add_field(name='По статусам:', value=f"""
<:online:979549939573088286> В сети: **{online_count}**
<:idle:979549885969883226> Не активен: **{idle_count}**
<:dnd:979549808631107664> Не беспокоить: **{dnd_count}**
<:offline:979549976797511680> Не в сети: **{offline_count}**""", inline=True)
        embed.add_field(name="Каналы:", value=f"""
<:channels_total:979727101181710366> Всего: **{len(ctx.guild.channels)}**
<:text_channel:979727123730296845> Текстовых: **{len(ctx.guild.text_channels)}**
<:voice_channel:979727132198576148> Голосовых: **{len(ctx.guild.voice_channels)}**""", inline=True)
        embed.add_field(name="Владелец:", value=ctx.guild.owner, inline=True)
        embed.add_field(name="Уровень проверки:", value=verification_level, inline=True)
        embed.add_field(name='Дата создания:', value=f"""
<t:{int(ctx.guild.created_at.timestamp())}:D>
<t:{int(ctx.guild.created_at.timestamp())}:R>""", inline=True)
        embed.set_footer(text=f"ID: {ctx.guild.id}")
        embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.respond(embed=embed)

def setup(client):
    print("Connect server.py")
    client.add_cog(Server(client))