import discord
from discord.ext import commands, tasks
import io
import os
from itertools import cycle
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
client = commands.Bot(command_prefix='.')
client.remove_command('help')
channel_id = int(os.getenv("CHANNEL_ID"))
status = cycle (["by @sooji & @kuntuy", "DM to send a menfess"])

@client.event
async def on_ready():
  print('{0.user} is on'.format(client))
  change_status.start()

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

async def pull_attachment(attachment):
    file = io.BytesIO()
    await attachment.save(file)
    return discord.File(file, filename=attachment.filename)

async def pull_files(abc):
    if len(abc) < 1:
        return
    elif len(abc) > 0:
        files = [await pull_attachment(attachment) for attachment in abc]
        return files

@client.command()
async def ping(ctx):
  await ctx.send('pong')

@client.command()
async def ct(ctx):
    if ctx.message.guild != None:
        return
    channel1 = client.get_channel(channel_id)
    archived_threads = channel1.archived_threads()
    archived_threads = await archived_threads.flatten()
    index = int(len(channel1.threads) + len(archived_threads)+ 1)
    if index < 10:
        index = "00" + str(index)
    elif index >= 10 and index <100:
        index = "0" + str(index)
    message_content = str(ctx.message.content)
    del1 = message_content.replace(f".{str(ctx.command.name)} ", "", 1)
    sent_message = f"__**{index}**__: {del1}"
    thread_name = f"{index}: {del1}"
    files = await pull_files(ctx.message.attachments)
    message = await channel1.send(sent_message, files=files)
    await message.create_thread(name = thread_name)

@client.command()
async def rt(ctx, index):
    if ctx.message.guild != None:
        return
    elif len(index) != 3:
        await ctx.send("index format incorrect")
        return
    channel1 = client.get_channel(channel_id)
    archived_threads = channel1.archived_threads()
    archived_threads = await archived_threads.flatten()
    thread_id = [thread.id for thread in channel1.threads if thread.name.startswith(str(index))] + [thread.id for thread in archived_threads if thread.name.startswith(str(index))]
    if len(thread_id) < 1:
        await ctx.channel.send("Thread not found")
    elif len(thread_id) > 0:
        thread = await client.fetch_channel(int(thread_id[0]))
        message_content = str(ctx.message.content)
        del1 = message_content.replace(f".{str(ctx.command.name)} ", "", 1)
        del2 = del1.replace(f"{str(index)} ", "", 1)
        files = await pull_files(ctx.message.attachments)
        await thread.send(del2, files=files)

@client.command()
async def m(ctx):
    if ctx.message.guild != None:
        return
    channel1 = client.get_channel(channel_id)
    message_content = str(ctx.message.content)
    del1 = message_content.replace(f".{str(ctx.command.name)} ", "", 1)
    files = await pull_files(ctx.message.attachments)
    msg = await channel1.send('**Menfess:** '+del1, files=files)
    await msg.add_reaction('❤️')

@client.command()
async def tampol(ctx, member:discord.User=None):
  if (member == ctx.message.author or member == None):
      await ctx.send(f"{ctx.message.author.mention} menampol diri sendiri!") 
  else:
      await ctx.send(f"{ctx.message.author.mention} menampol {member.mention}!")  

@client.command()
async def github(ctx):
  await ctx.send('https://github.com/irfanalmsyah/Ilkomerz58-Menfess')
  await ctx.send('https://replit.com/@irfanalmsyah/Ilkomerz58-Menfess')

@client.command()
async def gangerti(ctx):
  await ctx.send("""
.m <text> | bikin menfess tanpa thread
.ct <judul thread> | bikin menfess pake thread
.rt <thread index> <text> | reply ke thread pakai bot
.tampol <user> | tampol
.github | show the bot github repository
  """)

keep_alive()  
client.run (os.getenv("TOKEN"))
