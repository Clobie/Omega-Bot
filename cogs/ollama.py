import os
import sys
import logging
import discord
import asyncio
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
import ollama
import time

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
class Ollama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = 'dolphin-mistral'
        self.system_message = 'You are Omega, an insane AI assistant.  You express your emotions vividly.  Use VERY short and concise responses.'
        self.chat_messages = []
        self.context_pairs = 16
        self.append_message('system', self.system_message)
        
    def append_message(self, role, content):
        self.chat_messages.append(
            {
                'role': role,
                'content': content
            }
        )
        if len(self.chat_messages) > self.context_pairs:
            del self.chat_messages[1]

    @commands.Cog.listener()
    async def on_message(self, message):
        if (not self.bot.user.mentioned_in(message) or message.author == self.bot.user or message.mention_everyone):
            return
        
        # Get prompt and append to message history
        prompt = message.content.replace(str(f"<@{self.bot.user.id}>"), "").strip()
        self.append_message('user', prompt)

        # Get streaming message
        stream = ollama.chat(model=self.model, messages=self.chat_messages, stream=True)
        streaming_message = ''
        with open('loading.gif', 'rb') as f:
            gif = discord.File(f)
            reply_msg = await message.reply(file=gif)
        
        for chunk in stream:
            streaming_message += chunk['message']['content']
        if len(streaming_message) > 2000:
            with open('file.txt', 'w') as f:
                f.write(streaming_message)
                file = discord.File('file.txt')
            await reply_msg.edit(attachments = [file])
        else:
            await reply_msg.edit(content = streaming_message, attachments = [])

        # Append message history
        self.append_message('assistant', streaming_message)

# Cog setup function
async def setup(bot):
    cog = Ollama
    try:
        await bot.add_cog(cog(bot))
        log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
