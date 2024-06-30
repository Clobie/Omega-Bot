import logging
import discord
from discord.ext import commands, tasks
import subprocess
import json
from includes import logger as log

class GameDig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status.start()

    @tasks.loop(minutes=1)
    async def update_status(self):
        try:
            result = subprocess.run(
                ['node', './includes/digger.js'],
                capture_output=True,
                text=True,
                check=True
            )

            server_data = json.loads(result.stdout.strip())
            status_messages = []

            for server in server_data:
                if server['status'] == 'online':
                    status_message = f"🟢 {server['name']}: {server['players']}/{server['maxPlayers']}"
                else:
                    status_message = f"🔴 {server['name']}: Offline"
                status_messages.append(status_message)

            final_status = "\n".join(status_messages)
            if len(final_status) > 128:
                final_status = " | ".join(status_messages)

            await self.bot.change_presence(activity=discord.Game(name=final_status))

        except subprocess.CalledProcessError as e:
            log.log(f"Error calling digger.js: {e.stderr}", level=logging.ERROR)
        except json.JSONDecodeError as e:
            log.log(f"Failed to parse JSON from digger.js: {str(e)}", level=logging.ERROR)

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    cog = GameDig
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
