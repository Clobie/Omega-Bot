import os
import sys
import logging
import discord
import pyqrcode
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
from includes import config
from includes import logger as log

# Cog class
class QR(commands.Cog, name="qr"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="qr")
    async def my_command(self, context, *, msg):
        """
        Generates a QR code from entered text.
        """
        qrobj = pyqrcode.create(msg)
        qrobj.png('qr.png', scale=8)
        await context.send(file=discord.File('qr.png'))
        os.remove("qr.png")

# Cog setup function
async def setup(bot):
    cog = QR
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
