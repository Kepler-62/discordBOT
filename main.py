import discord
import discord.utils
from fuzzywuzzy import fuzz
import requests
import asyncio
import json
from fuzzywuzzy import process
import os
from const import *


with open("token.txt", "r") as f:
    TOKEN = f.read()


class MyClient(discord.Client):
    async def spam(self, message):
        for channel in self.get_all_channels():
            print(channel)
            try:
                await channel.send(message.content[5:])
            except Exception:
                continue

    async def weather(self, message):
        weather_token = "67faa5a552a1f272e9b244ae2a696b8d"
        try:
            city = message.content.split()[1]
            request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric")
            data = request.json()

            city = data['name']
            current_weather = data['main']['temp']
            water = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']

            await message.channel.send(f"Погода в городе {city}: \nТемпература: {current_weather}\nВлажность: {water}\nДавление: {pressure}\nСкорость ветра: {wind}")
        except Exception:
            await message.channel.send("Ты что-то не так написал")


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
            await self.mute(message, author=True)
            await asyncio.sleep(5)
            await self.unmute(message, author=True)


    async def mute(self, message, author=False):
        role = discord.utils.get(message.guild.roles, id=969861323968102410)
        if author:
            user = message.author
        else:
            user = message.mentions[0]
        await user.add_roles(role)
        await message.channel.send(f"Доступ к текстовому каналу для {user} ограничен")

    async def unmute(self, message, author=False):
        role = discord.utils.get(message.guild.roles, id=969861323968102410)
        if author:
            user = message.author
        else:
            user = message.mentions[0]
        await user.remove_roles(role)
        await message.channel.send(f"Доступ к текстовому каналу для {user} возобновлен")

    async def choice(self, message):
        request = requests.get("https://yesno.wtf/api")
        response = request.json()
        print(response)
        await message.channel.send(response['image'])

    async def on_message(self, message):
        if message.author == client.user:
            return

        for hello in HELLO_LIST:
            if message.content.startswith(hello):
                await message.channel.send('Мяу...')

        if message.content.startswith("!mute"):
            user = message.mentions[0]
            await self.mute(message)

        if message.content.startswith("!unmute"):
            await self.unmute(message)

        if message.content.startswith("!warning"):
            await self.warning(message)

        if message.content.startswith("!spam"):
            await self.spam(message)

        if message.content.startswith("!choice"):
            await self.choice(message)

        if message.content.startswith("!weather"):
            await self.weather(message)

        if fuzz.partial_ratio(message.content.lower(), BAD_WORDS) >= 60:
            await message.channel.send("На этом канале не ругаются>:(")
            await self.warning(message, author=True)
            await message.delete()


client = MyClient()

client.run(TOKEN)