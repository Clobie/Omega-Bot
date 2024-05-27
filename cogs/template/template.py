import os
import sys
import logging
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt

# Set up directory structure
CWD = os.getcwd()
DIR_INCLUDES = os.path.join(CWD, "includes")
DIR_COGS = os.path.join(CWD, "cogs")
DIR_LOGS = os.path.join(CWD, "logs")
CONFIG_FILE = os.path.join(DIR_INCLUDES, "config.py")
os.makedirs(DIR_LOGS, exist_ok=True)

# Set up logging
logging.basicConfig(
    filename=os.path.join(DIR_LOGS, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Logging function
def log(message, level=logging.INFO):
    formatted_message = logging.getLogger('').handlers[0].format(
        logging.makeLogRecord(
            {'msg': message, 'levelname': logging.getLevelName(level)}
        )
    )
    print(formatted_message)
    {
        logging.WARNING: lambda: logging.warning(message),
        logging.ERROR: lambda: logging.error(message)
    }.get(level, lambda: logging.info(message))()


# Import configuration
if not os.path.isfile(CONFIG_FILE):
    log(f"'{CONFIG_FILE}' not found, exiting", logging.ERROR)
    sys.exit()
else:
    from includes import config

# Cog class
class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    # Listener: Runs when bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        log(f'Logged in as {self.bot.user}')
    
    # Listener: Runs when a message is received
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "hello" in message.content.lower():
            await message.channel.send(f'Hello, {message.author.mention}!')
            log(f'Sent hello message to {message.author}')

    # Command: Responds with 'Pong!' and bot's latency
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with 'Pong!' and the bot's latency."""
        latency = self.bot.latency
        await ctx.send(f'Pong! Latency: {latency*1000:.2f} ms')
        log(f'Responded to ping command with latency {latency*1000:.2f} ms')

    # Task loop: Repeats a task on the interval
    @tasks.loop(minutes=1.0)
    async def my_task(self):
        now = dt.now(dt.UTC)
        channel = self.bot.get_channel(config.YOUR_CHANNEL_ID)
        if channel:
            await channel.send(f'Current time: {now.strftime("%Y-%m-%d %H:%M:%S")} UTC')
            log(f'Sent time to channel {config.YOUR_CHANNEL_ID}')

    @my_task.before_loop
    async def before_my_task(self):
        log('Waiting for bot to be ready...')
        await self.bot.wait_until_ready()

# Cog setup function
async def setup(bot):
    cog = MyCog
    try:
        await bot.add_cog(cog(bot))
        log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
