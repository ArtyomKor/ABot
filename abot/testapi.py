import discord
from discord.ext import commands
from discord.ui import Modal, InputText

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
        await interaction.response.send_message(embeds=[embed])
        
class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		
    @commands.slash_command(name="testmodal", guild_ids=[940119996477095986])
    async def test(self, ctx):
        modal = MyModal(title="Это ABot, детка!")
        await ctx.interaction.response.send_modal(modal)
       
def setup(bot):
    bot.add_cog(Test(bot))