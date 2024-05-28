import os
import sys
import logging
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
from includes import config
from includes import logger as log
from flask import Flask, request, jsonify, render_template
from threading import Thread
import asyncio

# Cog class
class WebApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = Flask(__name__)
        self.thread = Thread(target=self.run_flask)
        self.thread.start()

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/send_message', methods=['POST'])
        def send_message():
            data = request.json
            if 'channel_id' in data and 'message' in data:
                channel_id = data['channel_id']
                message = data['message']
                asyncio.run_coroutine_threadsafe(self.send_message_to_channel(channel_id, message), self.bot.loop)
                return jsonify({"status": "success", "message": "Message sent"}), 200
            else:
                return jsonify({"status": "error", "message": "Invalid data"}), 400

    def run_flask(self):
        self.app.run(host='0.0.0.0', port=5000)

    async def send_message_to_channel(self, channel_id, message):
        channel = self.bot.get_channel(int(channel_id))
        if channel:
            await channel.send(message)

# Cog setup function
async def setup(bot):
    cog = WebApp
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
