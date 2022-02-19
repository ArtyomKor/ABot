import discord
from discord.ext import commands
from discord.ui import Modal, InputText

class MyModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Short Input", placeholder="Placeholder Test"))

        self.add_item(
            InputText(
                label="Longer Input",
                value="Longer Value\nSuper Long Value",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Your Modal Results", color=discord.Color.random())
        embed.add_field(name="First Input", value=self.children[0].value, inline=False)
        embed.add_field(name="Second Input", value=self.children[1].value, inline=False)
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