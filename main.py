import discord
from discord.ui import view
from discord.ext import commands
import random
import time
from datetime import datetime
from datetime import date
from discord_slash import SlashCommand, SlashContext
import json
import qrcode
from PIL import Image
import os
from bs4 import BeautifulSoup
import requests
from discord_components import DiscordComponents, Button, ButtonStyle
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from itertools import cycle
from discord.ext import tasks, commands
from discord.utils import get
import asyncio
import youtube_dl
import re
import urllib
from gtts import gTTS
from pytube import YouTube
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands

mysongs = ['https://www.youtube.com/watch?v=pIPBphyOIB4', 'https://www.youtube.com/watch?v=mCxcQWdiR84', 'https://www.youtube.com/watch?v=Y7QBY5OrkmM', '']
prefix = '.b '
client = commands.Bot(command_prefix = prefix, help_command = None, intents = discord.Intents.all())  #bot prefix, is there really that much to explain?
guild_ids = [932013886658449428]
slash = SlashCommand(client)
players = {}
status = cycle(['Music is here!','More features soon!', 'I swear that i am working on this.', 'Please add me to your server, i would love that', f'{prefix}help', 'Still in early development', 'Developed and hosted by the one and only TuNisiAa559#6819'])
paused = False
list_to_play = []
song_queue = []
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@client.event
async def on_ready(): #things that run at the start of the bot
    print(f'{client.user} has connected to Discord!')  # prints in chat when the bot gets online
    song = 'Never gonna give you up" - Rick Astley'
    change_status.start()
    date_object = date.fromtimestamp(time.time())
    now = datetime.now()
    current_time = str(now.strftime("%H:%M:%S") +' '+ str(date_object))
    with open('logs.txt', 'a') as a:
        a.write(f"[{current_time}] Bot connected\n")

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_message(message : discord.Message):  #things that run each time someone sends a message



    try:
        username = str(message.author).split("#")[0]
    except:
        username = "nfu"
    
    msg = str(message.content)
    if msg == "":
        msg = "[Embed]"
    else:
        pass
    
    date_object = date.fromtimestamp(time.time())
    now = datetime.now()
    current_time = str(now.strftime("%H:%M:%S") +' '+ str(date_object))
    channel = str(message.channel)
    server = str(message.guild)
    print(f"[{current_time}] user: {username}, msg: {msg}, channel: {channel}, server: {server}")  #prints username,message,channel and server whenever someone sends a message

    await client.process_commands(message)

@slash.slash(name="help", description="Need some help?")
async def _help(ctx: SlashContext):
    embedVar = discord.Embed(
        title="Help arrived!",
        description="Here are a list of commands for your help",
        colour=(0xff0000))
    embedVar.add_field(name="Bot Prefix", value=prefix, inline=False)
    embedVar.add_field(name="Moderation Commands", value="help, say, mute", inline=True)
    embedVar.add_field(name="Fun commands", value="toss, randomnumber", inline=True)
    embedVar.set_thumbnail(
        url=        "https://media.discordapp.net/attachments/923531605660815373/974248483479494686/charizard-mega-charizard-y.gif"
    )
    print(f'help used by {ctx.author}')
    await ctx.channel.send(embed=embedVar)

@client.command()
async def help(ctx):
    user = discord.Member
    embed1 = discord.Embed(title="Bot commands help", url="https://discord.com/oauth2/authorize?client_id=726826901825519617&permissions=8&scope=bot%20applications.commands", description='To prevent this bot from flooding chats,\ninformation about commands has been sent to you directly.', color=0xFF0000)
    embed1.set_footer(text = "If you are encountering issues, please contact TuNisiAa559#6819.")
    embed2 = discord.Embed(title = "Bot commands help", url = "https://discord.com/oauth2/authorize?client_id=726826901825519617&permissions=8&scope=bot%20applications.commands", description = '-dm [user] [message content]  anonymously message someone in your server.\n\n-rickroll  sends per of the lyrics to the famous song by Rick Astley.\n\n-mute [user]  adds a "muted" role to whoever you ping.\n\n-kick [user] kicks whoever you ping.\n\n-ban [user] bans whoever you ping.\n\n-blacklist [word]  blacklists a word, if anyone says this word they will get warned, after the third time they get kicked after the server.\n\n-join/-leave  joins or leaves the voice chat that you are in and does absolutely nothing.', color = 0x0f9633)
    embed2.set_footer(text = "If you are encountering issues, please contact TuNisiAa559#6819.")
    await ctx.send(embed=embed1)
    await ctx.author.send(embed = embed2)


@client.command()
async def joinmessage(ctx):
    with open("joinmessage.json", "r") as write_file:
        a = json.dump("data", write_file)
        print(str(a))


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    while True :
        await channel.connect()
        await ctx.send("Connected!")

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Disconnected!")

@client.command()
async def dm(ctx, user : discord.Member, message = None):
    if user != None:
        await user.send(message)
        await ctx.send(f"{str(user).split('#')[0]} has received the message")
    else:
        await ctx.send("something went wrong")

@client.command()
async def rickroll(ctx, user : discord.Member):
    channel = user.voice.channel
    if channel != None:
        await channel.connect()
        player = await YTDLSource.from_url(url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await user.send("```Never gonna give you up \nNever gonna let you down \nNever gonna run around and desert you \nNever gonna make you cry \nNever gonna say goodbye \nNever gonna tell a lie and hurt you```")

@client.command()
async def mute(ctx, user : discord.Member):
    if user != None and ctx.message.author.guild_permissions.administrator == True:
        secks = discord.utils.get(ctx.guild.roles , id = 943248099361579078)
        await user.add_roles(secks)
        await ctx.send(f"{str(user).split('#')[0]} has been muted")   
        await user.move_to(channel = 964836837560573982)
    else:
        await ctx.send("Something went wrong, or you don't have the permissions for that.")

@client.command()
async def kick(ctx, user : discord.Member):
    if user != None and ctx.message.author.guild_permissions.administrator == True:
        await user.kick()
        await ctx.send(f"{str(user).split('#')[0]} has been kicked")
    else:
        await ctx.send("Something went wrong, or you don't have the permissions for that.")

@client.command()
async def ban(ctx, user : discord.Member):
    if user != None and ctx.message.author.guild_permissions.administrator == True:
        await user.ban()
        await ctx.send(f"{str(user).split('#')[0]} has been banned")
    else:
        await ctx.send("Something went wrong, or you don't have the permissions for that.")

@client.command()
async def unban(ctx, user : discord.Member):
    if user != None and ctx.message.author.guild_permissions.administrator == True:
        await user.unban()
        await ctx.send(f"{str(user).split('#')[0]} has been unbanned")
    else:
        await ctx.send("Something went wrong, or you don't have the permissions for that.")


@client.command()
async def createrole(ctx, message = None):
    if user != None and ctx.message.author.guild_permissions.administrator == True:
        await ctx.guild.create_role(name = message)
        await ctx.send("You successfully created a role!")
    else:
        await ctx.send("Something went wrong, or you don't have the permissions for that.")

@client.command()
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Current latency is  `{int(ping)}ms`")

@client.command()
async def user(ctx, user : discord.Member , guild = discord.Guild):
    if user != None:
        username = str(user).split('#')[0]
        roles = []
        for user_role in user.roles:
            roles.append(user_role.mention)
        roles.pop(0)
        embed = discord.Embed(title = f'Username : "{username}"', description = '' , color = 0x63c9ff)
        embed.set_thumbnail(url = user.avatar_url)
        embed.add_field(name='Roles in "' + str(ctx.message.guild.name) + '":', value=roles, inline=False)
        print(user.avatar_url)
        await ctx.send(embed=embed)
    else:
        ctx.send("Please mention somebody when using this command, if you are trying to see your stats, try using the stats command.")

@client.command()
async def stats(ctx, guild = discord.Guild):
    username = str(ctx.message.author).split('#')[0]
    roles = []
    for user_role in ctx.message.author.roles:
        roles.append(user_role.mention)
    roles.pop(0)
    embed = discord.Embed(title = f'Username : "{username}"', description = '' , color = 0x63c9ff)
    embed.set_thumbnail(url = ctx.message.author.avatar_url)
    embed.add_field(name='Roles in "' + str(ctx.message.guild.name) + '":', value=roles, inline=False)
    print(ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()    
async def av(ctx, user : discord.Member , guild = discord.Guild):
    username = str(user).split('#')[0]
    embed = discord.Embed(title = f"{username}'s avatar :", color = 0x63c9ff)
    embed.set_image(url = user.avatar_url)
    embed.set_footer(text = f'command used by {ctx.message.author}', icon_url = ctx.message.author.avatar_url)
    print(user.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def bmi(ctx, *, content):
    msg = str(content).split(" ")
    print(msg)
    height = float(msg[0])/100
    weight = float(msg[1])
    bmi = round(weight/height/height, 2)
    color = 0xffff00
    if bmi > 30.0:
        color = 0xff0000
        description = "You are severely overweight, we highly recommend you see a doctor."
    elif bmi > 25.0:
        pass
        description = "You are overweight, you might consider seeing a doctor, but you are not obese yet."
    elif bmi > 18.5:
        color = 0x008000
        description = "Your weight is pretty good compared to your height, this is only an indication though, so remember to always maintain a healthy lifestyle."
    
    embed = discord.Embed(title = f"Your BMI is {bmi}",description = description, color = color)
    embed.set_footer(text = f'command used by {ctx.message.author}', icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = embed)

@client.command()
async def qr(ctx, *, content):
    msg = str(content)
    qr = qrcode.make(msg)
    qr.save(f"qr{ctx.message.author}.png")
    await ctx.send(file = discord.File(f"qr{ctx.message.author}.png"))
    os.remove(f"qr{ctx.message.author}.png")

@client.command()
async def ttt(ctx, user : discord.Member):
    embed = discord.Embed(title = f"{str(ctx.message.author).split('#')[0]} is challenging {str(user).split('#')[0]} to a tictactoe game!", description = "")
    await user.send(embed = embed)
    await ctx.send(embed = embed)
    
    class TicTacToe:

        def __init__(self):
            self.board = []

        def create_board(self):
            self.board = []
            for i in range(3):
                row = []
                for j in range(3):
                    row.append('-')
                self.board.append(row)

        async def get_random_first_player(self):
            return random.randint(0, 1)

        async def fix_spot(self, row, col, player):
            self.board[row][col] = player

        async def is_player_win(self, player):
            win = None

            n = len(self.board)

            # checking rows


            for i in range(n):
                win = True
                for j in range(n):
                    if self.board[i][j] != player:
                        win = False
                        break
                if win:
                    return win

            # checking columns
            for i in range(n):
                win = True
                for j in range(n):
                    if self.board[j][i] != player:
                        win = False
                        break
                if win:
                    return win

            # checking diagonals
            win = True
            for i in range(n):
                if self.board[i][i] != player:
                    win = False
                    break
            if win:
                return win

            win = True
            for i in range(n):
                if self.board[i][n - 1 - i] != player:
                    win = False
                    break
            if win:
                return win
            return False

            for row in self.board:
                for item in row:
                    if item == '-':
                        return False
            return True

        async def is_board_filled(self):
            for row in self.board:
                for item in row:
                    if item == '-':
                        return False
            return True

        async def swap_player_turn(self, player):
            return user if player == ctx.message.author else ctx.message.author

        async def start(self):
            self.create_board()
            self.board = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
            player = str(ctx.message.author).split('#')[0] if await self.get_random_first_player() == 1 else str(user).split('#')[0]
            while True:
                await ctx.send(content = f"Player **{player}** turn", components=[[Button(style=ButtonStyle.gray, label=self.board[0], custom_id="button1", disabled = False), Button(style=ButtonStyle.gray, label=self.board[1], custom_id="button2"), Button(style=ButtonStyle.gray, label=self.board[2], custom_id="button3", disabled = False)], [Button(style=ButtonStyle.gray, label=self.board[3], custom_id="button4", disabled = False), Button(style=ButtonStyle.gray, label=self.board[4], custom_id="button5"), Button(style=ButtonStyle.gray, label=self.board[5], custom_id="button6", disabled = False)], [Button(style=ButtonStyle.gray, label=self.board[6], custom_id="button7", disabled = False), Button(style=ButtonStyle.gray, label=self.board[7], custom_id="button8"), Button(style=ButtonStyle.gray, label=self.board[8], custom_id="button9", disabled = False)]] )
                notplayer = not player
                # taking user input
                while True:
                    interaction = await client.wait_for("button_click", check = lambda i: i.component.user)
                
                if interaction.user == player:
                    await ctx.send(f'You pressed {interaction.component.custom_id}')
                    if interaction.component.custom_id == "button1":
                        row, col = list(map(int, [1, 1]))
                    elif interaction.component.custom_id == "button2":
                        row, col = list(map(int, [1, 2]))
                    elif interaction.component.custom_id == "button3":
                        row, col = list(map(int, [1, 3]))
                    elif interaction.component.custom_id == "button4":
                        row, col = list(map(int, [2, 1]))
                    elif interaction.component.custom_id == "button5":
                        row, col = list(map(int, [2, 2]))
                    elif interaction.component.custom_id == "button6":
                        row, col = list(map(int, [2, 3]))
                    elif interaction.component.custom_id == "button7":
                        row, col = list(map(int, [3, 1]))
                    elif interaction.component.custom_id == "button8":
                        row, col = list(map(int, [3, 2]))
                    elif interaction.component.custom_id == "button9":
                        row, col = list(map(int, [3, 3]))
                else:
                    await ctx.send(f"Cheating won't work, wait for your turn {notplayer}")

                # fixing the spot
                self.fix_spot(row - 1, col - 1, player)

                # checking whether current player is won or not
                if self.is_player_win(player):
                    await ctx.send(f"Player {player} wins the game!")
                    break

                # checking whether the game is draw or not
                if self.is_board_filled():
                    await ctx.send("Match Draw!")
                    break

                # swapping the turn
                player = self.swap_player_turn(player)

            # showing the final view of board
            await ctx.send(content = f"Player **{player}** turn", components=[[Button(style=ButtonStyle.gray, label=self.board[0], custom_id="button1", disabled = True), Button(style=ButtonStyle.gray, label=self.board[1], custom_id="button2", disabled = True), Button(style=ButtonStyle.gray, label=self.board[2], custom_id="button3", disabled = True)], [Button(style=ButtonStyle.gray, label=self.board[3], custom_id="button4", disabled = True), Button(style=ButtonStyle.gray, label=self.board[4], custom_id="button5", disabled = True), Button(style=ButtonStyle.gray, label=self.board[5], custom_id="button6", disabled = True)], [Button(style=ButtonStyle.gray, label=self.board[6], custom_id="button7", disabled = True), Button(style=ButtonStyle.gray, label=self.board[7], custom_id="button8", disabled = True), Button(style=ButtonStyle.gray, label=self.board[8], custom_id="button9", disabled = True)]] )


    # starting the game
    tic_tac_toe = TicTacToe()
    await tic_tac_toe.start()

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Blurple Button",style=discord.ButtonStyle.blurple) # or .primary
    async def blurple_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Gray Button",style=discord.ButtonStyle.gray) # or .secondary/.grey
    async def gray_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Green Button",style=discord.ButtonStyle.green) # or .success
    async def green_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Red Button",style=discord.ButtonStyle.red) # or .danger
    async def red_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Change All",style=discord.ButtonStyle.success)
    async def color_changing_button(self,child:discord.ui.Button,interaction:discord.Interaction):
        for child in self.children:
            child.disabled=True
        await interaction.response.edit_message(view=self)
            
@client.command()
async def button(ctx):
    view=Buttons()
    view.add_item(discord.ui.Button(label="URL Button",style=discord.ButtonStyle.link,url="https://github.com/lykn"))
    await ctx.send("This message has buttons!",view=view)

@client.command()
async def args(ctx, *args):
    await ctx.send('`{}` arguments: `{}`'.format(len(args), ', '.join(args)))

async def playa(ctx,url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':   'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1   -reconnect_streamed 1 -reconnect_delay_max 5',  'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()


@tasks.loop(seconds=3)
async def play_the_list():
    global list_to_play
    if paused == False:
        if len(list_to_play) != 0:
            ctx = list_to_play[0][1]
            voice = get(client.voice_clients, guild=ctx.guild)
            if voice.is_playing() == False:
                if len(list_to_play) != 0:
                    await playa(list_to_play[0][1],list_to_play[0][0])
                    del list_to_play[0]
            

@client.command(aliases = ["stop"])
async def pause(ctx):
    channel = ctx.message.guild
    voice_channel = channel.voice_client                
    voice_channel.pause()

@client.command()
async def resume(ctx):
    channel = ctx.message.guild
    voice_channel = channel.voice_client  
    voice_channel.resume()

@client.command()
async def skip(ctx):
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command(aliases = ['paly', 'plya', 'aply', 'alpy', 'ytsong'])
async def play(ctx, *, content):
    avatar = ctx.message.author
    if content.startswith('https://www.youtube.com/watch?v=') == False and content.startswith('https://www.youtube.com/playlist?list=') == False:
        search_keyword=content.replace(' ', '+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        song_queue.append(url)
        image_id = video_ids[0]
    else:
        url = content
        song_queue.append(url)
        image_id = url.replace("https://www.youtube.com/watch?v=", "")
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    async with ctx.typing():
        if voice != None:
            if voice.is_playing():
                while song_queue[0] != None:
                    player = await YTDLSource.from_url(url = song_queue[0], loop=client.loop, stream=True)
                    time.sleep(YouTube(song_queue[0]).lenght)
                    ctx.voice_client.disconnect()
            else:
                player = await YTDLSource.from_url(url = song_queue[0], loop=client.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                embed = discord.Embed(title = f'Now playing **{player.title}**',url = url)
                embed.set_thumbnail(url = 'http://img.youtube.com/vi/'+ image_id +'/maxresdefault.jpg')
                embed.set_footer(text = f'Command used by {avatar}')
                await ctx.send(embed = embed)
                time.sleep(YouTube(song_queue[0]).lenght)
                song_queue.pop(0)
                ctx.voice_client.disconnect()
        else:
                voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.send("Connected!")
                await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
                player = await YTDLSource.from_url(url = song_queue[0], loop=client.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                embed = discord.Embed(title = f'Now playing **{player.title}** ``',url = url)
                embed.set_thumbnail(url = 'http://img.youtube.com/vi/'+ image_id +'/maxresdefault.jpg')
                embed.set_footer(text = f'Command used by {avatar}')
                await ctx.send(embed = embed)
                time.sleep(YouTube(song_queue[0]).lenght)
                song_queue.pop(0)
                ctx.voice_client.disconnect()

client.run('NzI2ODI2OTAxODI1NTE5NjE3.GZvqjr.YoV2Edp8st4i180jnE1n39YNvaVj5ht_zsDSmY')
