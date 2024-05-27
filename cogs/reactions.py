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

class RandomReact(commands.Cog, name="random_emoji"):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_list = [
            "\U0001F600", "\U0001F601", "\U0001F602", "\U0001F603", "\U0001F604", "\U0001F605",
            "\U0001F606", "\U0001F607", "\U0001F608", "\U0001F609", "\U0001F60A", "\U0001F60B",
            "\U0001F60C", "\U0001F60D", "\U0001F60E", "\U0001F60F", "\U0001F610", "\U0001F611",
            "\U0001F612", "\U0001F613", "\U0001F614", "\U0001F615", "\U0001F616", "\U0001F617",
            "\U0001F618", "\U0001F619", "\U0001F61A", "\U0001F61B", "\U0001F61C", "\U0001F61D",
            "\U0001F61E", "\U0001F61F", "\U0001F620", "\U0001F621", "\U0001F622", "\U0001F623",
            "\U0001F624", "\U0001F625", "\U0001F626", "\U0001F627", "\U0001F628", "\U0001F629",
            "\U0001F62A", "\U0001F62B", "\U0001F62C", "\U0001F62D", "\U0001F62E", "\U0001F62F",
            "\U0001F630", "\U0001F631", "\U0001F632", "\U0001F633", "\U0001F634", "\U0001F635",
            "\U0001F636", "\U0001F637", "\U0001F638", "\U0001F639", "\U0001F63A", "\U0001F63B",
            "\U0001F63C", "\U0001F63D", "\U0001F63E", "\U0001F63F", "\U0001F640"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if random.randint(1, 25) == 1:
            random_emoji = random.choice(self.emoji_list)
            await message.add_reaction(random_emoji)


# Cog setup function
async def setup(bot):
    cog = RandomReact
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
