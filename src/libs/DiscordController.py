import discord
import asyncio

class DiscordController(object):

    # Private Variables
    _voice_channel = None
    _bot_token = None
    _command_callback = None

    # Public Variables
    client = discord.Client()
    connected = False

    def __init__(self, bot_token, command_callback):
        # self.client = discord.Client()
        self._bot_token = bot_token
        self._command_callback = command_callback if command_callback else self._default_callback
        # if (command_callback):
        #     self._command_callback = command_callback
        # else:
        #     self


    def _default_callback(self, command="", args=[], source=None):
        pass

    def run(self):
        self.client.run(self._bot_token)

    @client.event
    async def on_ready():
        print("Discord login successful: " + self.client.user.name)
        self.connected = True

    @client.event
    async def on_message(message):
        print(message.content)
