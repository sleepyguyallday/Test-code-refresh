import discord
from discord.ext    import commands
from discord.ext.commands   import Bot
import asyncio
 
bot = commands.Bot(command_prefix='summon')

token = open("Token_PepsiBot.txt","r").read()

@bot.event
async def on_ready():
    print ("Ate Shawie is Ready")
 
 #something is wrong here since it keeps on outputing the second elif
@bot.event
async def on_message(message):
    if "hello there" in message.content.lower():
    	await bot.send_message(message.channel ,"General Kenobi!")
	
    elif "kamusta na" in message.content.lower():
    	await bot.send_message(message.channel ,"Dito, pagod pa rin sa buhay")

    elif "ano pa" in message.content.lower():
    	await bot.send_message(message.channel ,"Uyyyy, sira pa rin laptop ko")

    elif "tulog na ako guys" in message.content.lower():
    	await bot.close
    	
    else:
    	print("wala langg")

bot.run(token)