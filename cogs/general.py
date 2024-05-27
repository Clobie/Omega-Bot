import os
import sys
import logging
from discord.ext import commands

# Set up directory structure
CWD = os.getcwd()
DIR_INCLUDES = os.path.join(CWD, "includes")
CONFIG_FILE = os.path.join(DIR_INCLUDES, "config.py")
DIR_LOGS = os.path.join(CWD, "logs")
os.makedirs(DIR_LOGS, exist_ok=True)
DIR_COGS = os.path.join(CWD, "cogs")

# Configure logging
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
class General(commands.Cog):
    """
    This cog handles various tasks such as event listeners and utility functions.
    """
    def __init__(self, bot):
        self.bot = bot
    
    # General ping command
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with 'Pong!' and the bot's latency."""
        latency = self.bot.latency
        await ctx.send(f'Pong! Latency: {latency*1000:.2f} ms')
        log(f'Responded to ping command with latency {latency*1000:.2f} ms')
    
    # Listener: Runs when bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        log(f'Logged in as {self.bot.user}')
    
    # Command error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            #await ctx.send('Command not found.')
            log(f'Command not found: {ctx.message.content}', logging.ERROR)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument.')
            log(f'Missing required argument in command: {ctx.message.content}', logging.ERROR)
        else:
            await ctx.send('An error occurred.')
            log(f'An error occurred: {str(error)}', logging.ERROR)
            raise error
    
    @commands.Cog.listener()
    async def on_command(self, ctx):
        server_name = ctx.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = ctx.channel.name.encode('unicode_escape').decode('utf-8')
        command_content = ctx.message.content.encode('unicode_escape').decode('utf-8')
        log(f"Command '{command_content}' entered by {ctx.author} in {server_name} ({channel_name})", logging.INFO)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        server_name = ctx.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = ctx.channel.name.encode('unicode_escape').decode('utf-8')
        command_content = ctx.message.content.encode('unicode_escape').decode('utf-8')
        log(f"Command '{command_content}' completed by {ctx.author} in {server_name} ({channel_name})", logging.INFO)

    @commands.Cog.listener()
    async def on_message(self, message):
        server_name = message.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = message.channel.name.encode('unicode_escape').decode('utf-8')
        command_content = message.content.encode('unicode_escape').decode('utf-8')
        log(f"Message from {message.author} in {server_name} ({channel_name}): {command_content}", logging.INFO)

    
    # Edit logger
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        server_name = before.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = before.channel.name.encode('unicode_escape').decode('utf-8')
        before_content = before.content.encode('unicode_escape').decode('utf-8')
        after_content = after.content.encode('unicode_escape').decode('utf-8')
        log(f"Message edited by {before.author} in {server_name} ({channel_name}):"
            f"\nBefore: {before_content}"
            f"\nAfter: {after_content}", logging.INFO)

# Cog setup function
async def setup(bot):
    cog = General
    try:
        await bot.add_cog(cog(bot))
        log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
