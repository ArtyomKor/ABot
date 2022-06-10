import discord
from discord.ext import commands
import sqlite3

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect('db/abot.db')
        self.sql = self.db.cursor()
        print("events.py connected!")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        await self.client.change_presence(activity=discord.Game('шпиона'), status=discord.Status.idle)
        print('Подключен...')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        start_message = await guild.system_channel.send(content='Спасибо за то, что добавили меня! Пожалуйста, подождите пока я выполню первоначальные настройки. Не выключайте сервера Discord.')
        try:
            self.sql.execute(f'CREATE TABLE IF NOT EXISTS "{guild.id}"(user_id BIGINT, bio TEXT DEFAULT "Тут ничего нет! Но Вы можете добавить сюда свой текст с помощью команды /bio", voice_name TEXT DEFAULT {None});')
            for i in guild.members:
                self.sql.execute(f'INSERT INTO "{guild.id}"(user_id) VALUES (?)', (i.id,))
            self.db.commit()
            await start_message.edit(content="Ура! Всё готово! Теперь я могу включить будильник... Извиняюсь, это был не мой текст. С полным перечнем команд и их описанием Вы можете ознакомиться с помощью комманды /help. Также не забудьте спрятать админ команды от всех, кроме модераторов или админов.")
        except Exception as error:
            await start_message.edit(content="Странно! Что-то пошло не так и первоначальные настройки не могут быть выполнены! Мы уже разбираемся с этим...")
            self.sql.execute('INSERT INTO bugs VALUES (?, ?)', (guild.id, error, "register"))
            self.db.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.sql.execute(f"""INSERT INTO "{member.guild.id}"(user_id) VALUES (?)""", (member.id, ))
        self.db.commit()

async def setup(client):
    print("Connect events.py")
    await client.add_cog(Events(client))