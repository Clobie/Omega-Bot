import os
import sys
import logging
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
from includes import config
from includes import logger as log

class RoleSelectionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = None  # Initialize role message ID here
        self.emoji_to_role = {
            "🐍": "Python",
            "🟦": "JavaScript",
            "☁️": "Cloud",
            "📱": "Mobile Development",
            "🎮": "Game Development",
            "🖥️": "Desktop Development",
            "🌐": "Web Development",
            "🤖": "Automation",
            "📊": "Data Science",
            "🔐": "Cybersecurity",
            "📡": "Networking",
            "🖨️": "Hardware",
            "🎨": "2D Artist",
            "🖌️": "3D Artist",
            "🎬": "Animation",
            "🎵": "Audio Engineering",
            "📝": "Technical Writing",
            "🛠️": "DevOps",
            "🧪": "QA / Testing",
            "📈": "Business Intelligence",
            "💼": "Project Management",
            # Add more emoji-role mappings as needed
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot connected as {self.bot.user}')
        try:
            guild = self.bot.get_guild(1187101350941700166)
            if guild:
                welcome_channel = guild.get_channel(1256857017516167250)
                if welcome_channel:
                    # Send the role selection message
                    message = await welcome_channel.send(
                        "Welcome! React to this message to select your roles:\n"
                        "🐍 for Python\n"
                        "🟦 for JavaScript\n"
                        "☁️ for Cloud\n"
                        # Add more instructions here
                    )
                    self.role_message_id = message.id

                    # Add reactions to the message
                    for emoji in self.emoji_to_role.keys():
                        await message.add_reaction(emoji)
                else:
                    print(f"Could not find welcome channel with ID {1256857017516167250}")
            else:
                print(f"Could not find guild with ID {1187101350941700166}")
        except Exception as e:
            print(f"An error occurred during on_ready: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.role_message_id:
            try:
                guild = self.bot.get_guild(payload.guild_id)
                if guild:
                    role_name = self.emoji_to_role.get(payload.emoji.name)
                    if role_name:
                        role = discord.utils.get(guild.roles, name=role_name)
                        if role:
                            member = guild.get_member(payload.user_id)
                            if member:
                                await member.add_roles(role)
                                print(f'Assigned {role_name} role to {member.display_name}')
            except Exception as e:
                print(f"An error occurred during on_raw_reaction_add: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.role_message_id:
            try:
                guild = self.bot.get_guild(payload.guild_id)
                if guild:
                    role_name = self.emoji_to_role.get(payload.emoji.name)
                    if role_name:
                        role = discord.utils.get(guild.roles, name=role_name)
                        if role:
                            member = guild.get_member(payload.user_id)
                            if member:
                                await member.remove_roles(role)
                                print(f'Removed {role_name} role from {member.display_name}')
            except Exception as e:
                print(f"An error occurred during on_raw_reaction_remove: {e}")

async def setup(bot):
    cog = RoleSelectionCog
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
