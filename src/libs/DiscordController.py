import discord
import re

# Private Variables
_voice_channel = None
_command_callback = None
_command_id = "~"
_flag_id = "-"
_command_re = re.compile('^' + _command_id + '(\w+)')
_flag_and_contents = re.compile('^(\w+)\W*(.*)')


# Public Variables
client = discord.Client()
discord_connected = False

def _default_callback(command="", args=[], source=None):
    pass

def discord_init(secrets, command_callback=None):
    global _bot_name
    # Get name of bot so we can ignore messages it sends
    _bot_name = secrets["botName"] # "JukeBot"
    # Currently not in use
    _command_callback = command_callback if command_callback else _default_callback

# Start the discord client THIS IS BLOCKING!!!
def run_discord(bot_token):
    client.run(bot_token)

# Execute on bot discord login
@client.event
async def on_ready():
    print("Discord login successful: " + client.user.name)
    discord_connected = True

# Text-channel message event
@client.event
async def on_message(message):
    # Ignore messages from this bot to avoid infinite callbacks
    if message.author.name == _bot_name:
        return

    # callee = function_possibilities.get(message.content)
    # if not callee:
    #     await client.send_message(message.channel, "I can't do that, " + message.author.name)
    # else:
    #     await callee(message)
    print(_parse_message(message.content))

# Dummy test function
async def test(message):
    await client.send_message(message.channel, "I am test and I heard: " + message.content)

# Test if message meets the criteria for a command
def _is_command(message_content):
    return _command_re.match(message_content) != None

# Parse message, withdrawing command and flags if possible
def _parse_message(message_content):
    parsed_message = {}
    # If message indeed is a command...
    if (_is_command(message_content)):
        # Grab the command itself
        parsed_message["command"] = _command_re.match(message_content).group(1)
        parsed_message["flags"] = []
        # Split on flag_id for flag/flag-argument sections
        command_args = message_content.split(_flag_id)
        # Everything before first flag_id is ignored (probably just command)
        for i in range(1, len(command_args)):
            # Add to flags list if flag found in split token
            match = _flag_and_contents.match(command_args[i])
            if match != None:
                parsed_message["flags"].append({})
                parsed_message["flags"][i-1]["flag"] = match.group(1)
                parsed_message["flags"][i-1]["contents"] = match.group(2)

    return parsed_message

function_possibilities = globals().copy()
function_possibilities.update(locals())
