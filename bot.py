import os
import discord
from dotenv import load_dotenv
from database import create_table, add_message
import datetime

# load virtual environment variables
load_dotenv()

# get token and guild name from .env file
APP_TOKEN = os.getenv('DISCORD_APP_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')


# change this according to your need
keywords = ["?TSLA", "?AAPL", "?FCBK"]


# create a discord client for our bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
create_table()

@client.event
async def on_ready():
    """This method will be run when the client is ready"""
    
    try:
        guild = next(filter(lambda g: str(g.id) == str(GUILD_ID), client.guilds))
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name} (id: {guild.id})'
        )
    except:
        raise ValueError("Couldn't connect to the server, please check `DISCORD_GUILD_ID` value in `.env`")


@client.event
async def on_message(message):
    """This method execute when a new message come"""

    # check if the message is from the bot itself, don't change this
    if message.author == client.user:
        return

    # print new incoming message
    print(f'Message from {message.author}: {message.content}')

    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%d %I:%M %p")

    add_message(message.author.name, message.content, message.author.guild.name, str(time))
    await message.channel.send("Hi! I'm a bot, Thanks for messaging!")

@client.event
async def on_error(event, *args, **kwargs):
    """ Handle error, if anything get error """
    with open('logs/error.log', 'a+') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(APP_TOKEN)
