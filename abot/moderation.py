import discord
from discord.ext import commands
from discord.commands import Option
from discord.ui import Button, View
from config import owner_id, moder_id
import random

code = random.randint(0, 999999999)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="shutdown", description="Выключение бота.")
    async def shutdown(self, ctx, код: Option(str, 'Код доступа.', required=False, default=None)):
        emb = discord.Embed(title="Выключение", colour=discord.Color.red())
        member = self.bot.get_user(owner_id)
        if str(код) == str(code):
            await ctx.respond(embed=emb)
            raise SystemExit(1)
        elif код == None:
            await member.send("/shutdown " + str(code))
            emb.add_field(name='Ошибка', value='Не обнаружен код доступа, пожалуйста, введите его. Высылаю код.')
        elif код := str(code):
            emb.add_field(name='Ошибка', value='Код неверный! Введите корректный код.')
        await ctx.respond(embed=emb)

    @commands.slash_command(name='clear', description='Очистить чат.')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, количество: Option(int, 'Количество удаляемых сообщений.', required=False, default=100)):
        if количество >= 1000000000000:
            await ctx.respond('Максимальное количество: 100000000000')
        else:
            messages = await ctx.history(limit=1000000000000).flatten()
            await ctx.channel.purge(limit=количество)
            if len(messages) >= количество:
                if количество >= 5:
                    await ctx.respond(f'Удалено {количество} сообщений!')
                if количество >= 2 and количество <= 4:
                    await ctx.respond(f'Удалено {количество} сообщения!')
                elif количество == 1:
                    await ctx.respond(f'Удалено 1 сообщение!')

            if len(messages) <= количество:
                if len(messages) >= 5:
                    await ctx.respond(f'Удалено {len(messages)} сообщений!')
                if len(messages) >= 2 and len(messages) <= 4:
                    await ctx.respond(f'Удалено {len(messages)} сообщения!')
                elif len(messages) == 1:
                    await ctx.respond(f'Удалено 1 сообщение!')

    @commands.slash_command(name='admin', description='Админ панель')
    @commands.has_role(moder_id)
    async def admin(self, ctx, пользователь: Option(discord.Member, 'Пользователь', required=True)):
        id = пользователь.id
        role = discord.utils.get(ctx.guild.roles, id=923522612066418769)
        emb = discord.Embed(title='Админ-панель', colour=discord.Color.green())
        emb.add_field(name='Действия', value=f'Что Вы хотите сделать с {пользователь.display_name}?')
        kickB = Button(label='Кикнуть', style=discord.ButtonStyle.danger,row=1)
        async def kick_callback(interaction):
            await interaction.response.edit_message(content="Кикнут(а)!", view=None, embed=None)
            await пользователь.kick(reason=f'ABot, с наилучшими пожеланиями от {ctx.author.display_name}')
        kickB.callback = kick_callback
        if role in пользователь.roles:
            muteB = Button(label='Размьютить', style=discord.ButtonStyle.success,row=1)
        else:
            muteB = Button(label='Замьютить', style=discord.ButtonStyle.danger,row=1)
        async def mute_callback(interaction):
            if role in пользователь.roles:
                await interaction.response.edit_message(content="Размьючен(а)!", view=None, embed=None)
                await пользователь.remove_roles(role, reason=f'ABot, с наилучшими пожеланиями от {ctx.author.display_name}')
            else:
                await interaction.response.edit_message(content="Замьючен(а)!", view=None, embed=None)
                await пользователь.add_roles(role, reason=f'ABot, с наилучшими пожеланиями от {ctx.author.display_name}')
        muteB.callback = mute_callback
        banB = Button(label='Забанить', style=discord.ButtonStyle.danger,row=1)
        async def ban_callback(interaction):
            await interaction.response.edit_message(content="Забанен(а)!", view=None, embed=None)
            await пользователь.ban(reason=f'ABot, с наилучшими пожеланиями от {ctx.author.display_name}')
        view = View()
        view.add_item(kickB)
        view.add_item(muteB)
        view.add_item(banB)
        await ctx.respond(embed=emb,view=view)

    async def addorremove(ctx: discord.AutocompleteContext):
        vibor=["убрать", "поставить"]
        return [
            выбор for выбор in vibor
        ]

    @commands.slash_command(name='ёлка', description='Поставить или убрать ёлки с ника')
    @commands.has_permissions(administrator=True)
    async def elka(self, ctx, выбор: Option(str,"Поставить или убрать, вот в чём вопрос...",autocomplete=discord.utils.basic_autocomplete(addorremove))):
        owner = self.bot.get_user(int(ctx.guild.owner.id))
        server_members = ctx.guild.members
        owindex = server_members.index(owner)
        server_members.pop(owindex)
        if выбор == "убрать":
            await ctx.respond('Начинаю...')
            for i in server_members:
                name = i.display_name
                new_name = name.replace("🎄", "")
                await i.edit(nick=new_name)
        elif выбор == "поставить":
            await ctx.respond('Начинаю...')
            for i in server_members:
                name = i.display_name
                new_name = "🎄"+ name + "🎄"
                await i.edit(nick=new_name)
        else:
            await ctx.respond('Выберите: убрать или поставить.')
        
def setup(bot):
    bot.add_cog(Moderation(bot))

