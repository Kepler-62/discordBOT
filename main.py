import discord
import discord.utils
import os
from const import *


with open("token.txt", "r") as f:
    TOKEN = f.read()


class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author == client.user:
            return

        for hello in HELLO_LIST:
            if message.content.startswith(hello):
                await message.channel.send('Мяу...')

        if message.content.startswith("!mute"):
            role = discord.utils.get(message.guild.roles, id=962041876041564240)
            user = message.mentions[0]
            await user.add_roles(role)
            await message.channel.send(f"Доступ к текстовому каналу для {user} ограничен")

        if message.content.startswith("!unmute"):
            role = discord.utils.get(message.guild.roles, id=962041876041564240)
            user = message.mentions[0]
            await user.remove_roles(role)
            await message.channel.send(f"Доступ к текстовому каналу для {user} возобновлен")



client = MyClient()

client.run(TOKEN)