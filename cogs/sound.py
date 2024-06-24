import logging
import discord
from discord import FFmpegPCMAudio
import asyncio
from discord.ext import commands
from includes import logger as log
from includes import config
import time

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test(self, ctx):
        user = ctx.message.author
        voice_channel = user.voice.channel
        
        if voice_channel:
            try:
                voice_client = await voice_channel.connect()
                audio_source = FFmpegPCMAudio('test.mp3')
                voice_client.play(audio_source)
                while voice_client.is_playing():
                    await asyncio.sleep(1)
                await voice_client.disconnect()
            except discord.ClientException as e:
                await ctx.send(f"Error: {e}")

            while voice_client.is_playing() or voice_client.is_paused():
                await time.sleep(1)

            await voice_client.disconnect()
        else:
            await ctx.send("User is not in a voice channel.")

async def setup(bot):
    cog = MyCog
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
