import discord

from .utils.activity import ActivityRotation

import logging
import json


config = json.load(open("./data/config.json", "r"))
logger = logging.getLogger('discord.main')
logger.setLevel(config['log']['level'].upper())

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user} (ID: {client.user.id})')
    activity = ActivityRotation(client, config['bot']['activities']);

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(f'{config['bot']['prefix']}ping'):
        await message.reply(f'pong! ({client.latency * 1000:.2f}ms)')
    elif message.content.startswith(f'{config['bot']['prefix']}'):
        await message.reply('Hello! I\'m currently under development. That means I don\'t do much yet and whatever you just tried to do won\'t work. Please be patient!')

client.run(config['bot']['token']);