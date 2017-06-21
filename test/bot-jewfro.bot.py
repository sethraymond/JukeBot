import discord
import asyncio
import json
from libs.gmusic import GpmSession

with open("../secrets/bot-jewfro.secret.json", "r") as secrets_file:
    secrets = json.load(secrets_file)

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global voicech
    global voice
    global player

    if message.content.startswith('&joinvoice'):
        voicech = message.content.split(' ')[1]
        all_channels = list(client.get_all_channels())
        for ch in all_channels: #TODO: if no arg, make bot look to see where user currently is
            if str(ch) == voicech and ch.type == discord.ChannelType.voice:
                voicech = ch
        print(str(voicech), voicech.type)
        voice = await client.join_voice_channel(voicech)
        voice.connect()
    elif message.content.startswith('&newsong'):
        title_search = None
        artist_search = None
        search_terms = message.content.split('&')
        if len(search_terms) > 2:
            title_search = search_terms[2]
        if len(search_terms) > 3:
            artist_search = search_terms[3]
        url = session.get_song_stream(title_search, artist_search)
        if not url:
            await client.send_message(message.channel, "Song ain't found, yo.")
        else:
            #requires user to run `export PATH=$PATH:/usr/bin/avconv` or wherever avconv is installed
            player = await voice.create_ytdl_player(url, use_avconv=True) 
            player.volume = 0.1
            player.start()
    elif message.content.startswith('&stop'):
        player.stop()
    elif message.content.startswith('&leavevoice'):
        await voice.disconnect()
    elif message.content.startswith('&pause'):
        player.pause()
    elif message.content.startswith('&resume'):
        player.resume()
    elif message.content.startswith('&setvolume'):
        vol = float(message.content.split(' ')[1])
        player.volume = vol
    elif message.content.startswith('&isvoiceconnected'):
        status = voice.is_connected() 
        print(status)

session = GpmSession(secrets["gPlayAppUser"], secrets["gPlayAppPass"])
while not session.logged_in:
    session = GpmSession()
client.run(secrets["botToken"])
