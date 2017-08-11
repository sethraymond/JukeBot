#!/usr/bin/python3

import json
import asyncio
from libs.DiscordController import *
import libs.GooglePlayMusicController as GPMController

# Load secrets
with open("../secrets/JukeBot.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

gpm = GPMController.GpmSession(secrets["gPlayAppUser"], secrets["gPlayAppPass"])
while not gpm.logged_in:
    gpm = GPMController.GpmSession()

# DYNAMIC FUNCTIONS START HERE

async def test(options):
    print(options)
async def getsong(options):
    global url
    if gpm.api.is_subscribed:
        song_title = None
        song_artist = None
        song_album = None
        for option in options:
            if option["flag"] == "title":
                song_title = option["contents"]
            elif option["flag"] == "artist":
                song_artist = option["contents"]
            elif option["flag"] == "album":
                song_album = option["contents"]
        song = gpm.search_store(song_title, song_artist, song_album)
        song_id = gpm.add_song_to_library(song)
        url = gpm.api.get_stream_url(song_id)
        print(song_title, song_artist, song_album)

# DYNAMIC FUNCTIONS END HERE
# These MUST be after the dynamic functions
function_possibilities = globals().copy()
function_possibilities.update(locals())

# Callback for DiscordController so this bot can execute commands entered in chat
async def _discord_callback(parsed_message, original_message):
    # Attempt to find function in this file with a name that matches the command
    callee = function_possibilities.get(parsed_message["command"])
    if not callee:
        # Function not found: complain to user
        await respond(original_message, "I can't do " + parsed_message["command"] + ", " + original_message.author.name)
    else:
        # Function found: call it with the command flags
        await callee(parsed_message["flags"])

# Init discord
discord_init(secrets, _discord_callback)


# Blocking, run last
run_discord(secrets["botToken"])

gpm.api.logout()
