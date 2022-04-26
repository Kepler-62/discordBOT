import discord
import music_config
from discord.ext import commands
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

client = commands.Bot(command_prefix='-')


@client.command()
async def play(ctx, *, arg):
    vc = await ctx.message.author.voice.channel.connect()

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in arg:
            info = ydl.extract_info(arg, download=False)
        else:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

    url = info['formats'][0]['url']

    vc.play(discord.FFmpegPCMAudio(executable="D:\discord_bot\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))


client.run(music_config.token)