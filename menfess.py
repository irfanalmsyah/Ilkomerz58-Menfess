'''
pls dont steal this code i wasted my time on this 
'''


import io
import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from itertools import cylce

client= commands.Bot(command_prefix = '$')
status = cycle (['DM to send a menfess', 'Made by Irfan Alamsyah'])

@client.event
async def on_ready():
  print('{0.user} is on'.format(client))
  change_status.start()
 
client.remove_command('help')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#$whoareyou
@client.command()
async def whoareyou(ctx):
  await ctx.send('I am {0.user} made by sooji#2905'.format(client))

@client.event
async def on_message(message):
    channel = client.get_channel(channel id here)
    if message.guild is None and message.author != client.user:
        has_attachments = message.attachments != []
        if has_attachments:
            async with channel.typing():
                files = [await pull_attachment(attachment) for attachment in message.attachments]
        else:
            files = None
        sent_message = await channel.send('Menfess: {}'.format(message.content), files=files))
    await client.process_commands(message)
    
async def pull_attachment(attachment):
    file = io.BytesIO()
    await attachment.save(file)
    return discord.File(file, filename=attachment.filename)

client.run (put bot token here)
