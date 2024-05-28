import os
import sys
import logging
from discord.ext import commands
from includes import config
from includes import logger as log

# Cog class
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # General ping command
    @commands.command(name='ping')
    async def ping(self, ctx):
        latency = self.bot.latency
        await ctx.send(f'Pong! Latency: {latency*1000:.2f} ms')
        log.log(f'Responded to ping command with latency {latency*1000:.2f} ms')
    
    # Listener: Runs when bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        log.log(f'Logged in as {self.bot.user}')
    
    # Command error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            log.log(f'Command not found: {ctx.message.content}', logging.ERROR)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument.')
            log.log(f'Missing required argument in command: {ctx.message.content}', logging.ERROR)
        else:
            await ctx.send(f'An error occurred: {str(error)}')
            log.log(f'An error occurred: {str(error)}', logging.ERROR)
            raise error
    
    @commands.Cog.listener()
    async def on_command(self, ctx):
        server_name = ctx.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = ctx.channel.name.encode('unicode_escape').decode('utf-8')
        command_content = ctx.message.content.encode('unicode_escape').decode('utf-8')
        log.log(f"Command '{command_content}' entered by {ctx.author} in {server_name} ({channel_name})", logging.INFO)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        server_name = ctx.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = ctx.channel.name.encode('unicode_escape').decode('utf-8')
        command_content = ctx.message.content.encode('unicode_escape').decode('utf-8')
        log.log(f"Command '{command_content}' completed by {ctx.author} in {server_name} ({channel_name})", logging.INFO)

    @commands.Cog.listener()
    async def on_message(self, message):
        server_name = message.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = message.channel.name.encode('unicode_escape').decode('utf-8')
        command_content = message.content.encode('unicode_escape').decode('utf-8')
        log.log(f"Message from {message.author} in {server_name} ({channel_name}): {command_content}", logging.INFO)

    
    # Edit logger
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        server_name = before.guild.name.encode('unicode_escape').decode('utf-8')
        channel_name = before.channel.name.encode('unicode_escape').decode('utf-8')
        before_content = before.content.encode('unicode_escape').decode('utf-8')
        after_content = after.content.encode('unicode_escape').decode('utf-8')
        log.log(f"Message edited by {before.author} in {server_name} ({channel_name}):"
            f"\nBefore: {before_content}"
            f"\nAfter: {after_content}", logging.INFO)

# Cog setup function
async def setup(bot):
    cog = General
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
