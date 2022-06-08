class VoiceCache:
    def __init__(self) -> None:
        self.channels = {}
        self.channels_name = {}
        print("Кэш голосовых каналов инициализирован!")

    async def append_channel(self, author, channel):
        try:
            self.channels[author] = channel
            return True
        except Exception as error:
            return error

    async def pop_channel(self, channel):
        for voice in list(self.channels.items()):
            if channel in voice:
                self.channels.pop(voice[0])

        
    async def append_channel_name(self, author, name, guild):
        try:
            self.channels_name[f"{guild}:{author}"] = name
            return True
        except Exception as error:
            return error