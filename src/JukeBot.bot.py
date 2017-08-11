#!/usr/bin/python3

# DYNAMIC FUNCTIONS START HERE

async def test(options):
    print(options)

# DYNAMIC FUNCTIONS END HERE
# These MUST be after the dynamic functions
function_possibilities = globals().copy()
function_possibilities.update(locals())

import json
import asyncio
from libs.DiscordController import *
import libs.GooglePlayMusicController as GPMController

# Load secrets
with open("../secrets/JukeBot.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

# Callback for DiscordController so this bot can execute commands entered in chat
async def _discord_callback(parsed_message):
    # Attempt to find function in this file with a name that matches the command
    callee = function_possibilities.get(parsed_message["command"])
    if not callee:
        # Function not found: complain to user
        # await client.send_message(message.channel, "I can't do " + parsed_message["command"] + ", " + message.author.name)
        pass
    else:
        # Function found: call it with the command flags
        await callee(parsed_message["flags"])

# Init discord
discord_init(secrets, _discord_callback)

gpm = GPMController.GpmSession(secrets["gPlayAppUser"], secrets["gPlayAppPass"])
while not gpm.logged_in:
    gpm = GPMController.GpmSession()
song = gpm.search_store("Hello", "Walk off the Earth")
song_id = gpm.add_song_to_library(song)
url = gpm.api.get_stream_url(song_id)

# Blocking, run last
run_discord(secrets["botToken"])

gpm.api.logout()
