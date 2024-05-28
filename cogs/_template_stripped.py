import logging
import discord
from discord.ext import commands
from includes import logger as log

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    cog = MyCog
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
