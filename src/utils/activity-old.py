# TODO:
# activity rotation

import discord

import asyncio
import logging
logger = logging.getLogger('utils.activity')

class Rotation:
    def __init__(self, client, activities):
        self.client = client
        self.activities = activities
        self.index = 0

    async def start(self):
        while True:
            await self.set_activity()
            await asyncio.sleep(20)
            self.next()

    def _build(self, activity):
        name = activity['name']
        match activity['type'].lower():
            case "playing":
                type = discord.ActivityType.playing
            case "streaming":
                type = discord.ActivityType.streaming
            case "listening":
                type = discord.ActivityType.listening
            case "watching":
                type = discord.ActivityType.watching
            case "competing":
                type = discord.ActivityType.competing
            case _:
                logger.warn(f'Unknown activity type: {activity['type']}. Using default \'playing\'.')
                type = discord.ActivityType.playing
        
        return discord.Activity(name=name, type=type)
    
    def _current(self):
        return self._build(self.activities[self.index])
    
    def _next(self):
        if self.index + 1 < len(self.activities):
            self.index += 1
        else:
            self.index = 0
    
    async def set_activity(self):
        await self.client.change_presence(activity=self._current())
        