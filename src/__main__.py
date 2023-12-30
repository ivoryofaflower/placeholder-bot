# TODO:
# - Implement activity + activity rotation
# - Respond to prefix with a template

import discord

from .utils.activity import ActivityRotation

import logging
import json


config = json.load(open("./data/config.json", "r"))
logger = logging.getLogger('discord.main')
logger.setLevel(config['log']['level'].upper())

# Intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user} (ID: {client.user.id})')
    activity = ActivityRotation(client, config['bot']['activities']);

client.run(config['bot']['token']);