"""
Change .env file with your bot's token and GUILD name

if you don't have any bot created yet, go here to create one
https://discord.com/developers/applications
create an application
then click the app you just created.
now from bot tab, create new bot and give the bot administation previlage
now copy the token and replace the token in .env file

* make sure the bot you have just created are added to your channel
"""










import os, csv
import discord
from dotenv import load_dotenv
from second import a, b
from discord import File
from table import get_output
from database import create_table, add_message
import datetime

# load virtual environment variables
load_dotenv()

# get token and guild name from .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# change this according to your need
keywords = ["?TSLA", "?AAPL", "?FCBK"]


# create a discord client for our bot
client = discord.Client()

@client.event
async def on_ready():
    """This method will be run when the client is ready"""
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    """This method execute when a new message come"""

    # check if the message is from the bot itself, don't change this
    if message.author == client.user:
        return

    # print new incoming message
    print('Message from {0.author}: {0.content}'.format(message))

    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%d %I:%M %p")

    create_table()
    add_message(message.author.name, message.content, message.author.guild.name, str(time))

    # check if the message content matches with any of the keywords
    if str(message.content).startswith("?"):
        if message.content in keywords:

            pdf_file = get_output(query=message.content)
            print("PDF:", pdf_file)
            with open(pdf_file, 'rb') as f:
                await message.channel.send(file=File(f, os.path.basename(pdf_file)))
            # await message.channel.send("a = " + str(a) + " b = "+str(b))
        else:
            await message.channel.send("Ticker doesn't exist.")

@client.event
async def on_error(event, *args, **kwargs):
    """ Handle error, if anything get error """
    with open('err.log', 'a+') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)