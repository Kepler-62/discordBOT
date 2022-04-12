import discord
import discord.utils
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
from const import *


with open("token.txt", "r") as f:
    TOKEN = f.read()


class MyClient(discord.Client):
    async def warning(self, message, author=False):
        if author:
            user = message.author
        else:
            user = message.mentions[0]

        if user in MEMBERS.keys():
            MEMBERS[user] += 1
        else:
            MEMBERS[user] = 1
        await message.channel.send(f"У {user} {MEMBERS[user]} из 5 предупреждений")

        if MEMBERS[user] == 5:
            await message.channel.send(f"{user} достиг(ла) максимального количества предупреждений")
            await self.mute(message)

    async def mute(self, message):
        role = discord.utils.get(message.guild.roles, id=962041876041564240)
        user = message.mentions[0]
        await user.add_roles(role)
        await message.channel.send(f"Доступ к текстовому каналу для {user} ограничен")

    async def unmute(self, message):
        role = discord.utils.get(message.guild.roles, id=962041876041564240)
        user = message.mentions[0]
        await user.remove_roles(role)
        await message.channel.send(f"Доступ к текстовому каналу для {user} возобновлен")

    async def on_message(self, message):
        if message.author == client.user:
            return

        for hello in HELLO_LIST:
            if message.content.startswith(hello):
                await message.channel.send('Мяу...')

        if message.content.startswith("!mute"):
            user = message.mentions[0]
            await self.mute(user)

        if message.content.startswith("!unmute"):
            user = message.mentions[0]
            await self.unmute(user)

        if message.content.startswith("!warning"):
            await self.warning(message)

        if fuzz.partial_ratio(message.content.lower(), BAD_WORDS) >= 50:
            await message.channel.send("На этом канале не ругаются>:(")
            await self.warning(message, author=True)
            await message.delete()



client = MyClient()

client.run(TOKEN)