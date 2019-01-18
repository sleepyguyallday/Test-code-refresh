# Ate Shawie Bot v1.0
# A bot made for our Dota2 server with the inspiration of Lorenzo Pepito's online persona: "Ate Shawie"
# This bot is still in the works of adding functions into it. For now, it is a music bot.
# The code is heavily based on svenBot in github. Please refer to the txt file where I placed the link of it.
# This bot is made as practice for automation in case I might need one to do when my taks become more complex
# For now, feel free to study it and use it on your server for music at least. Will do an update for memes later on.



# Setting up the libraries for the code to work here
import discord
import logging
import config

from youtube_dl import YoutubeDL
from discord.ext import commands

# Logs events in the console, will write to a file labelled as logs.txt
logging.basicConfig(filename='logs.txt' , level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this to see if it does work alright')
logging.warning('And this one might be necessary as well')

# Setting the class for the bot
client = commands.Bot(command_prefix = "shawie.")

# Lists that keeps track of volume, name and queued songs.
song_queue = []
song_name = []
song_volume = []

# Starts up the bot login sequence and prints out Ate Shawie's status.
@client.event
async def on_ready():
	print(f"[status] Ate Shawie is back betches!")

# Removes the commands from Discord after being executed - clearing up any clutter that might be made.
@client.event
async def on_message(message):
	if message.content.startswith("shawie."):
		await client.delete_message(message)
	await client.process_commands(message)

# Checks the queue for the media to play
def check_queue(ctx):
	song_queue.pop(0)
	song_name.pop(0)
	if song_queue:
		if song_volume:
			song_queue[0].volume = song_volume[0]
		client.loop.create_task(client.send_message(ctx.message.channel, f"**Playing queued video:** {song_name[0]}"))
		print(f"[status] Playing queued video: {song_name[0]}")
		song_queue[0].start()
	else:
		server = ctx.message.server
		song_queue.clear()
		song_name.clear()
		song_volume.clear()
		voice.client = client.voice_client_in(server)
		voice_client.loop.create_task(voice_client.disconnect())
		print(f"[status] Disconnected, no songs in queue")

# This will summon the bot and play media. If more than one action is made, it will queue for you.
@client.command(pass_context=True)
async def play (ctx, *, url):
	if "/playlist" in url:
		await client.say(f"You can't queue playlists")
	else:
		server = ctx.message.server
		if client.is_voice_connected(server):
			voice_client = client.voice_client_in(server)
		else:
			channel = ctx.message.author.voice.voice_channel
			await client.join_voice_channel(channel)
			voice_client = client.voice_client_in(server)

		player = await voice_client.create_ytdl_player(url, options=config.ydl_opts, after=lambda: check_queue(ctx), before_options=config.before_args)
		player.volume = 0.10

		if song_queue:
			song_queue.append(player)
			song_name.append(player.title)
			print(f"[status] Queuing: {player.title}")
			await client.say(f"**Queuing video**")
		else:
			song_queue.append(player)
			song_name.append(player.title)
			player.start()
			song_volume.append(song_queue[0].volume)
			print(f"[status] Playing: {player.title}")
			await client.say(f"**Playing:** {player.title}")

# Displays the current queue output
@client.command(pass_context=True)
async def queue(ctx):
	await client.say(f"___**Current Playlist___:**")
	for number, song in enumerate(song_name, 1):
		await client.say(f"{number}: {song}")

# Volume control stats: Change volume or disaplay current volume
@client.command(pass_context=True)
async def vol(ctx, *args):
	if song_queue:
		if not args:
			await client.say(f"**Current volume:** {int(song_volume[0] * 100)}%")
		elif int(args[0]) > 100:
			await client.say("**Can't go higher than 100% volume**")
		elif int (args[0]) <= 100:
			song_volume.clear()
			song_queue[0].volume = int(args[0]) / 100
			song_volume.append(song_queue[0].volume)
			await client.say(f"**Volume set to:**{str(args[0])}%")
		else:
			await client.say(f"**There's nothing playing, can't adjust volume**")

# Resumes paused player.
@client.command(pass_context=True)
async def resume(ctx):
	if song_queue:
		song_queue[0].resume()
		await client.say(f"**Resuming video**")
	else:
		await client.say(f"**There's nothing to resume**")

# Pauses the player
@client.command(pass_context=True)
async def pause(ctx):
	if song_queue:
		song_queue[0].pause()
		await client.say(f"**Pausing video**")
	else:
		await client.say(f"**There's nothing to pause here**")

# Makes the bot leave the current voice channel
@client.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	if client.voice_client_in(server):
		voice_client = client.voice_client_in(server)
		song_queue.clear()
		song_name.clear()
		song_volume.clear()
		await voice_client.disconnect()
		print(f"[status] Cleared queue and disconnected")
	else:
		await client.say(f"Can't leave if I'm not in a voice channel**")

# Skips the current song to the next song in queue.
@client.command(pass_context=True)
async def skip(ctx):
	if song_queue:
		song_queue[0].pause()
		check_queue(ctx)
		await client.say(f"**Skipping video**")
	else:
		await client.say(f"**There's nothing to skip**")

# Displays the list of available bot commands.
@client.command(pass_context=True)
async def botcommands(ctx):
	botcommands_list = [
	"___**Available commands for Ate Shawie Bot**___",
	"**shawie.play:** Plays/queue video, use URL or search string.",
	"**shawie.skip:** Skips the current song.",
	"**shawie.resume:** Resumes a paused song.",
	"**shawie.pause:** Pauses the current song.",
	"**shawie.leave:** Clears the queue and leaves voice channel.",
	"**shawie.queue:** Displays the current queue of songs.",
	"**shawie.vol:** Adjust the volume using a value between 1-100 (no value will output current volume)."

	]
	await client.say(f"\n".join(botcommands_list))

client.run(config.token)