#!/usr/bin/python3
import json
import asyncio
import discord
from libs.DiscordController import *
import libs.GooglePlayMusicController as GPMController

with open("../secrets/JukeBot.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

client = discord.Client()
gpm = GPMController.GpmSession(secrets["gPlayAppUser"], secrets["gPlayAppPass"])
while not gpm.logged_in:
    gpm = GPMController.GpmSession()
song = gpm.search_store("Hello", "Walk off the Earth")
song_id = gpm.add_song_to_library(song)
url = gpm.api.get_stream_url(song_id)

@client.event
async def on_message(message):
    global voice
    global player
    if message.content.startswith('&playsong'):
        for ch in list(client.get_all_channels()):
            if str(ch) == 'dev' and ch.type == discord.ChannelType.voice:
                voicech = ch
        voice = await client.join_voice_channel(voicech)
        voice.connect()
        player = await voice.create_ytdl_player(url, use_avconv = True)
        player.volume = 0.1
        player.start()
    elif message.content.startswith('&stop'):
        player.stop()
        await voice.disconnect()

gpm.api.logout()

client.run(secrets["botToken"])
