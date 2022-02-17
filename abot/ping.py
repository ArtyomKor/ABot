import discord
from discord.ext import commands
import datetime

mist_func="False"

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global mist_func
        mess = ''.join(i for i in message.content if not i.isalpha())
        print(mess)
        mess = mess.split()
        print(mess)
        if "<@891536476049899521>" in mess or "<@!891536476049899521>" in mess or "\\<@!891536476049899521>" in mess or "\\<@891536476049899521>" in mess:
            if message.author.id != 891536476049899521:
                try:
                    await message.author.timeout_for(duration=datetime.timedelta(minutes=5))
                    await message.channel.send(content=f"{message.author.mention}, ты его зачем звал?", delete_after=float(10))
                    await message.channel.send(content="https://cdn.discordapp.com/attachments/679090175132827679/779746133651095572/image0-1.gif", delete_after=float(10))
                except: pass
        for i in message.mentions:
            if 891536476049899521 == i.id:
                try:
                    await message.author.timeout_for(duration=datetime.timedelta(minutes=5))
                    await message.channel.send(content=f"{message.author.mention}, ты его зачем звал?", delete_after=float(10))
                    await message.channel.send(content="https://cdn.discordapp.com/attachments/679090175132827679/779746133651095572/image0-1.gif", delete_after=float(10))
                except: pass
        if message.content == "https://media.discordapp.net/attachments/796866823391543320/912296655200612362/gif_6.gif" and mist_func == "False" and message.author.id == 472723520372342814:
            mist_func = "True"
        if mist_func == "True" and message.author.id == 472723520372342814:
            mist_func = "False"
            try:
                id = ''.join(x for x in message.content if x.isdigit())
                print(id)
                user = await message.guild.fetch_member(int(id))
                await user.timeout_for(duration=datetime.timedelta(minutes=5))
                print(mist_func)
            except Exception as error:
                print(error)
                channel = await message.guild.fetch_channel(943834485332512818)
                await channel.send(content=f"Ой! Произошла ошибка!\n```{error}```")
        print(message.content)

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        await thread.join()

def setup(bot):
    bot.add_cog(Ping(bot))
