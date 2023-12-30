import discord

import json
import logging


config = json.load(open("./data/config.json", "r"))
logger = logging.getLogger('discord.main')
intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Logged in as {self.user} (ID: {self.user.id})')


client.run(config['bot']['token']);