import discord

# Private Variables
_voice_channel = None
_command_callback = None

# Public Variables
client = discord.Client()
discord_connected = False

def discord_init():
    # self._command_callback = command_callback if command_callback else self._default_callback
    # if (command_callback):
    #     self._command_callback = command_callback
    # else:
    #     self
    pass



def _default_callback(self, command="", args=[], source=None):
    pass

def run_discord(bot_token):
    client.run(bot_token)

@client.event
async def on_ready():
    print("Discord login successful: " + client.user.name)
    discord_connected = True

@client.event
async def on_message(message):
    print(message.content)
