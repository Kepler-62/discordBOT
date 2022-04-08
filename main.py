import discord
import os

client = discord.Client()
TOKEN = 'OTYxOTM2NzQxMjQwMDE2ODk2.YlAPZw.YEAJX7tAEbxkTAwyhNVvm8FGVD8'

hello_list = ["Привет!", "привет!", "Привет", "привет", "Салам алейкум", "hello", "guten tag"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Привет!') or :
        await message.channel.send('Мяу...')

client.run(TOKEN)
