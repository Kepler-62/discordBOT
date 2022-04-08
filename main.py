import discord
import os

client = discord.Client()
TOKEN = ''

hello_list = ["Привет!", "привет!", "Привет", "привет", "Салам алейкум", "hello", "guten tag"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for hello in hello_list:
        if message.content.startswith(hello):
            await message.channel.send('Мяу...')

client.run(TOKEN)
