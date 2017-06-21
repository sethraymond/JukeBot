#!/usr/bin/python3
import discord
import asyncio
import json
from libs.gmusic import GpmSession

with open("../secrets/botrumz.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('~test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'botrumz is calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('~sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith("~findurl"):
        titleSearch = None
        artistSearch = None
        searchTerms = message.content.split("~")
        if len(searchTerms) > 2:
            titleSearch = searchTerms[2]
        if len(searchTerms) > 3:
            artistSearch = searchTerms[3]
        url = session.get_song_stream(titleSearch, artistSearch)
        if not url:
            await client.send_message(message.channel, "NOTFOUND")
        else:
            await client.send_message(message.channel, url)

session = GpmSession(secrets["gPlayAppUser"], secrets["gPlayAppPass"])
while not session.logged_in:
    session = GpmSession()

client.run(secrets["botToken"])