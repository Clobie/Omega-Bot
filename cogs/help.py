import os
import sys
import logging
import discord
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
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help")
    async def help(self, context):
        """
        List commands
        """
        prefix = config.BOT_PREFIX
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="List of available commands and functionality:", color=config.success)
        for cog_name, cog_obj in self.bot.cogs.items():
            # Add cog description
            cogname = cog_name.replace("cog", "")
            if cog_obj.__doc__:
                embed.add_field(name=f"{cogname.capitalize()} - Description", value=cog_obj.__doc__.strip(), inline=False)
            commands = cog_obj.get_commands()
            commands_with_help = [(command.name, command.help) for command in commands if command.help]
            # Add commands with help descriptions
            if commands_with_help:
                command_list, command_description = zip(*commands_with_help)
                help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
                embed.add_field(name=f"{cogname.capitalize()} - Commands", value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)

# Cog setup function
async def setup(bot):
    cog = Help
    try:
        await bot.add_cog(cog(bot))
        log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
