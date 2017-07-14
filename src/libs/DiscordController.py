import discord

# Private Variables
_voice_channel = None
_command_callback = None

# Public Variables
client = discord.Client()
discord_connected = False

def _default_callback(command="", args=[], source=None):
    pass

def discord_init(secrets, command_callback=None):
    global _bot_name
    # _bot_name = secrets["botName"]
    _bot_name = "JukeBot"
    _command_callback = command_callback if command_callback else _default_callback

def run_discord(bot_token):
    client.run(bot_token)

@client.event
async def on_ready():
    print("Discord login successful: " + client.user.name)
    discord_connected = True

@client.event
async def on_message(message):
    if message.author.name == _bot_name:
        return
    callee = function_possibilities.get(message.content)
    if not callee:
        await client.send_message(message.channel, "I can't do that, " + message.author.name)
    else:
        await callee(message)

async def test(message):
    await client.send_message(message.channel, "I am test and I heard: " + message.content)

# function_possibilities = None
function_possibilities = globals().copy()
function_possibilities.update(locals())

