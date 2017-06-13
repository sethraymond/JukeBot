import discord
import asyncio
from gmusicapi import Mobileclient
import getpass

def gpm_login():
    email = input('Please enter an email address tied to a GPM account: ')
    pw = getpass.getpass('Please enter the password associated with %s: ' % email)
    logged_in = api.login(email, pw, Mobileclient.FROM_MAC_ADDRESS) #per api protocol
    if logged_in:
        print('Login successful!')
    else:
        print('Login failed! Please try again.')
    return logged_in

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('&test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('&sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

tokenFile = open("../tokens/bots/.discord-bot-token", "r")
token = tokenFile.readline().strip()

client = discord.Client()
api = Mobileclient()
while not gpm_login():
    pass
client.run(token)
