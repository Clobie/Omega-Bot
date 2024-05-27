import os
import sys
import discord
import logging
import asyncio
from discord.ext.commands import Bot
from datetime import datetime as dt
from includes import config
from includes import logger as log

# Initialize bot
intents = discord.Intents.all()
bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)
bot.remove_command("help")

# Command dispatch
@bot.event
async def on_message(message):
    if message.author is bot.user:
        return
    await bot.process_commands(message)

# Cog loading function
async def loadcogs():
    for filename in os.listdir(config.DIR_COGS):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog_name}')
            except Exception as e:
                log.log(f"Failed to load cog '{cog_name}': {str(e)}", logging.ERROR)

# Run bot
async def main():
    async with bot:
        await loadcogs()
        log.log("Waiting for the bot to be ready...")
        await bot.start(config.BOT_SECRETS_TOKEN)

asyncio.run(main())