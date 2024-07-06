import os
import sys
import logging
import discord
import re
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
from pytube import YouTube
from pytube import Playlist
from moviepy.editor import *
from pytube.innertube import _default_clients
from includes import config
from includes import logger as log

# Cog class
class Ripper(commands.Cog, name="ripper"):
    def __init__(self, bot):
        self.bot = bot
        _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

    def is_valid_youtube_url(self, url):
        youtube_regex = re.compile(
            r'^(https?://)?(www\.)?'
            r'(youtube\.com|youtu\.be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        
        match = youtube_regex.match(url)
        return match is not None

    @commands.command(name="rip")
    async def rip(self, context, url):
        """
        Youtube audio ripper.
        """
        if not self.is_valid_youtube_url(url):
            await context.send("Have you tried using an actual youtube link?")
            return

        ytlink = url.replace('https://', '')
        await context.send(f"Checking: {ytlink}")

        video = YouTube( 
            ytlink,
            use_oauth=True,
            allow_oauth_cache=True
        )

        audio = video.streams.filter(only_audio=True).first()
        size_mb = audio.filesize_mb
        if audio.filesize_mb >= 25:
            await context.send(f"File too large. {size_mb}mb")
        else:
            await context.send(f"Fetching: {ytlink}")
            out_file = audio.download()
            try:
                audiofile = discord.File(out_file)
                await context.send(file=audiofile)
            except:
                await context.send(f"Failed up attach.  Saved: {out_file.title}")
            os.remove(out_file)

# Cog setup function
async def setup(bot):
    cog = Ripper
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
