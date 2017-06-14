import discord
import asyncio
from libs.gmusic import GpmSession

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
    elif message.content.startswith('&joinvoice'):
        all_channels = list(client.get_all_channels())
        for ch in all_channels:
            if str(ch) == 'dev' and ch.type == discord.ChannelType.voice:
                voicech = ch
        print(str(voicech), voicech.type)
        voice = client.join_voice_channel(voicech)
    elif message.content.startswith('&leavevoice'):
        pass
    elif message.content.startswith('&isvoiceconnected'):
        pass

tokenFile = open("../tokens/bots/.discord-bot-token", "r")
token = tokenFile.readline().strip()

#session = GpmSession()
#while not session.logged_in:
#    session = GpmSession()
client.run(token)
