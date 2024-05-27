import os
import sys
import logging
import discord
from discord.ext import commands
from includes import config
from includes import logger as log

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
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
