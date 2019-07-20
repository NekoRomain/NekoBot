#BOT Created by NekoRomain 
#Twitter @NekoRomain

import discord
import os
import time
import youtube_dl
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description='MikuBot!')

vc = None
actualMusic = ""
TOKEN = #your_bot_token
ID_CHANNEL_MUSIC = #id_channel
musics = []
PATH = "./Musics/"
ydl_id_opt = PATH+'%(id)s.%(ext)s'
ydl_title_opt = PATH+'a.%(ext)s'
#ydl_title_opt = PATH+'%(title)s.%(ext)s'

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

# ydl_opts = {
#     'outtmpl': ydl_title_opt,
#     'format': 'bestaudio/best',
#     'download_archive': 'dl.txt',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
#     'progress_hooks': [my_hook],
# }

ydl_opts_webm = {
    'outtmpl': ydl_title_opt,
    'format': 'bestaudio/best',
    'progress_hooks': [my_hook],
}

@bot.event
async def on_ready():
    global vc
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-----")
    
    
@bot.command()
async def dlp(ctx, url):
    global vc, actualMusic
    if not vc or not vc.is_connected():
        await connectVocal()
    elif vc.is_playing() or vc.is_paused():
        if vc.is_playing():
            vc.pause()
            time.sleep(0.5)
        vc.stop()
        os.remove(actualMusic)
        actualMusic = ""

    with youtube_dl.YoutubeDL(ydl_opts_webm) as ydl:
        await ctx.send("Veuillez patienter... NYA~")
        info = ydl.extract_info(url)
        await ctx.send("Fini! NYA~")
        actualMusic = PATH + "a."+ info["ext"]
        await ctx.send("NOW PLAYING {} ! NYA~".format(info["title"]))
        vc.play(discord.FFmpegPCMAudio(actualMusic))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.25
        

@bot.command()
async def disconnect(ctx):
    global vc, actualMusic
    #channel = bot.get_channel(ID_CHANNEL_MUSIC)
    #for b in bot.voice_clients:
    #   await b.disconnect()
    if vc:
        if actualMusic:
            os.remove(actualMusic)
            actualMusic = ""
        await vc.disconnect()

async def connectVocal():
    global vc
    channel = bot.get_channel(ID_CHANNEL_MUSIC)
    try:
        vc = await channel.connect()
        if not discord.opus.is_loaded():
            discord.opus.load_opus()
    except commands.BotMissingPermissions as error:
        print("ERROR : {}".format(error))
    except discord.ClientException as error:
        print(error)

@bot.command()
async def connect(ctx):
    await connectVocal()

@bot.command()
async def vol(ctx, volume):
    global vc
    if volume >= "0" and volume <= "1" and vc:
        if vc.is_playing():
            vc.source.volume = float(volume)

@bot.command()
async def pause(ctx):
    global vc
    if vc:   
        if vc.is_playing():
            vc.pause()
            await ctx.send("MUSIQUE EN PAUSE NYA~")
        elif vc.is_paused():
            vc.resume()
            await ctx.send("REPRISE DE LA MUSIQUE NYA~")

@bot.command()
async def stop(ctx):
    global vc, actualMusic
    if vc:
        if vc.is_playing or vc.is_paused:
            vc.stop()
            os.remove(actualMusic)
            actualMusic = ""

@bot.command()
async def exit(ctx):
    global vc, actualMusic
    if vc:
        if vc.is_playing or vc.is_paused:
            if vc.is_playing():
                vc.pause()
                time.sleep(0.5)
            vc.stop()
            os.remove(actualMusic)
            actualMusic = ""
    return await bot.logout()

bot.run(TOKEN)

