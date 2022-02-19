import discord
from discord.ext import commands
from discord.ui import Modal, InputText

class MySelect(discord.ui.SelectMenu):
    def __init__(self):
        options = [
            discord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦')
        ]
        super().__init__(placeholder='Pick your colour', min_values=1, max_values=1, options=options)

    async def callback(self, interaction):
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}', ephemeral=True)


class MyModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Бомбящая жаба пидор", placeholder="Хуй соси"))

        self.add_item(
            InputText(
                label="Вывод как длина члена",
                value="Большой\nПрям очень большой",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Мнение опрошенных", color=discord.Color.random())
        embed.add_field(name="На что первым похуй", value=self.children[0].value, inline=False)
        embed.add_field(name="На что вторым", value=self.children[1].value, inline=False)
        embed.add_field(name="пикча", value=f"[Ссылка на изображение]({self.children[2].url})")
        await interaction.response.send_message(embeds=[embed])
        
class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		
    @commands.slash_command(name="testmodal", guild_ids=[940119996477095986])
    async def test(self, ctx):
        modal = MyModal(title="Это ABot, детка!")
        await ctx.interaction.response.send_modal(modal)
       
    @commands.slash_command(name="testselect", guild_ids=[940119996477095986])
    async def select(ctx):
        view = discord.ui.View()
        view.add_item(MySelect())
        await ctx.respond(content="bebra", view=view)

def setup(bot):
    bot.add_cog(Test(bot))