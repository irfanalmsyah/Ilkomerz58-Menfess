# spaghetti code
import discord
from discord.ext import commands
import io

intents = discord.Intents.all()

prefix="."
bot = commands.Bot(command_prefix=prefix, Intents=intents)

channel_id = {manually copy and put your channel id here}

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

@bot.command()
async def ct(ctx):
    if ctx.message.guild != None:
        return
    channel = bot.get_channel(channel_id)
    archived_threads = channel.archived_threads()
    archived_threads = await archived_threads.flatten()
    index = int(len(channel.threads) + len(archived_threads)+ 1)
    if index < 10:
        index = "00" + str(index)
    elif index >= 10 and index <100:
        index = "0" + str(index)
    message_content = str(ctx.message.content)
    del1 = message_content.replace(f".{str(ctx.command.name)} ", "", 1)
    sent_message = f"{index}: {del1}"
    files = await pull_files(ctx.message.attachments)
    message = await channel.send(sent_message, files=files)
    await message.create_thread(name = sent_message)

@bot.command()
async def rt(ctx, index):
    if ctx.message.guild != None:
        return
    elif len(index) != 3:
        await ctx.send("index format incorrect")
        return
    channel = bot.get_channel(channel_id)
    archived_threads = channel.archived_threads()
    archived_threads = await archived_threads.flatten()
    thread_id = [thread.id for thread in channel.threads if thread.name.startswith(str(index))] + [thread.id for thread in archived_threads if thread.name.startswith(str(index))]
    if len(thread_id) < 1:
        await ctx.channel.send("Thread not found")
    elif len(thread_id) > 0:
        thread = await bot.fetch_channel(int(thread_id[0]))
        message_content = str(ctx.message.content)
        del1 = message_content.replace(f".{str(ctx.command.name)} ", "", 1)
        del2 = del1.replace(f"{str(index)} ", "", 1)
        files = await pull_files(ctx.message.attachments)
        await thread.send(del2, files=files)

bot.run({put your bot token here})