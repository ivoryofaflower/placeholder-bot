import discord
from discord.ext import tasks

import logging
import json
config = json.load(open("./data/config.json", "r"))

class ActivityRotation:
    def __init__(self, bot, activities):
        self.bot = bot
        self.logger = logging.getLogger('discord.activity')
        self.logger.setLevel(config['log']['level'].upper())
        self.activities = activities
        self.index = 0
        self.logger.info(f'Initialized activity rotation with {len(self.activities)} activities')
        self.update_activity.start()

    @tasks.loop(seconds=config['bot']['activityDelay'])
    async def update_activity(self):
        activity = self._build_activity(self.activities[self.index])
        self.logger.debug(f'Updating activity... to {self.activities[self.index]}')
        await self.bot.change_presence(activity=activity)
        self.index = (self.index + 1) % len(self.activities)
    
    def _build_activity(self, activity):
        match activity['type'].lower():
            case 'playing':
                return discord.Game(name=activity['name'])
            case 'streaming':
                return discord.Streaming(name=activity['name'], url=activity['url'])
            case 'listening':
                return discord.Activity(name=activity['name'], type=discord.ActivityType.listening)
            case 'watching':
                return discord.Activity(name=activity['name'], type=discord.ActivityType.watching)
            case 'competing':
                return discord.Activity(name=activity['name'], type=discord.ActivityType.competing)
            case _:
                return discord.Activity(name=activity['name'], type=discord.ActivityType.unknown)

    def start(self):
        self.update_activity.start()

    def stop(self):
        self.update_activity.stop()
