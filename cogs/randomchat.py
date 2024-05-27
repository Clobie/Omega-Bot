import os
import sys
import logging
import discord
import random
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
from includes import config
from includes import logger as log

# Cog class
class RandomBeepBoop(commands.Cog, name="beep_boop"):    
    def __init__(self, bot):
        self.bot = bot
        self.random_channel_task.start()

    def cog_unload(self):
        self.random_channel_task.cancel()

    @tasks.loop(hours=random.randint(3, 6))
    async def random_channel_task(self):
        await self.bot.wait_until_ready()
        channels = self.bot.get_all_channels()
        random_channel = random.choice([channel for channel in channels if isinstance(channel, discord.TextChannel)])
        await random_channel.send("*Beep Boop*")

# Cog setup function
async def setup(bot):
    cog = RandomBeepBoop
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
