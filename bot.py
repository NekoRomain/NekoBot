#BOT Created by NekoRomain 
#Twitter @NekoRomain

import discord
import os
import time
import youtube_dl
from discord.ext import commands
vc = None

TOKEN = "#your token"
ID_CHANNEL_MUSIC = #ID_MUSIC_CHANNEL
musics = []
PATH = "./Musics/"
EXTENTION = ".webm"
ydl_id_opt = PATH+'%(id)s.%(ext)s'
ydl_title_opt = PATH+'%(title)s.%(ext)s'
bot = commands.Bot(command_prefix='!', description='MikuBot!')
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'outtmpl': ydl_title_opt,
    'format': 'bestaudio/best',
    'download_archive': 'dl.txt',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [my_hook],
}
ydl_opts_webm = {
    'outtmpl': ydl_title_opt,
    'format': 'bestaudio/best',
    'download_archive': 'dl.txt',
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
async def dl_yt(ctx, url):
    with youtube_dl.YoutubeDL(ydl_opts_webm) as ydl:
        await ctx.send("Veuillez patienter... NYA~")
        ydl.extract_info(url)
        await ctx.send("Fini! NYA~")


@bot.command()
async def play(ctx, arg):
    global vc
    if arg == "list":
        listMusic = ""
        i = 1
        musics.clear()
        for r, d, f in os.walk(PATH):
            for file in f:
                if EXTENTION in file:
                    musics.append(file)
                    listMusic += str(i) + " : " + file + "\n"
                    i +=1
        if listMusic == "":
            listMusic = "Aucune musique ~NYA"
        await ctx.send(listMusic)
    elif 0 < int(arg) <= len(musics):
        if len(musics) == 0:
            await ctx("Lancer d'abord !play list ~NYA")
            return
        if not vc or not vc.is_connected():
           await connectVocal()
        if vc.is_playing() or vc.is_paused():
            vc.stop()
        await ctx.send("PLAY! NYA~")
        vc.play(discord.FFmpegPCMAudio(PATH+musics[int(arg) - 1]))
        print("Music : {}".format(PATH+musics[int(arg) - 1]))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.25

#@bot.command()
#async def disconnect(ctx):
#    global vc
#    #channel = bot.get_channel(ID_CHANNEL_MUSIC)
#    #for b in bot.voice_clients:
#    #   await b.disconnect()
#    if vc:
#        await vc.disconnect()

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
    global vc
    if vc:
        if vc.is_playing or vc.is_paused:
            vc.stop()

@bot.command()
async def exit(ctx):
    return await bot.logout()

bot.run(TOKEN)

