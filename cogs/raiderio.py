import os
import sys
import logging
import discord
import requests
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
from includes import config
from includes import logger as log

# Cog class
class RaiderIO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rio")
    async def rio(self, context, msg):
        """
        Grabs raider.io character data.
        """
        async with context.typing():

            guild = requests.get(f"https://classic.raider.io/api/v1/characters/profile?region=us&realm=mankrik&name={msg.capitalize()}&fields=guild")
            guildjs = guild.json()
            character_guild = guildjs['guild']['name']
            character_honorable_kills = guildjs['honorable_kills']
            data = requests.get(f"https://classic.raider.io/api/v1/characters/profile?region=us&realm=mankrik&name={msg.capitalize()}&fields=gear")
            js = data.json()
            gear = js['gear']['items']
            thumbnail_url = js['thumbnail_url']
            profile_url = js['profile_url']
            character_ilvl_equipped = js['gear']['item_level_equipped']
            character_level = js['level']
            character_race = js['race']
            character_class = js['class']
            character_faction = js['faction']
            character_region = js['region']
            character_realm = js['realm']
            character_last_updated = js['last_crawled_at']
            character_gear_last_updated=js['gear']['updated_at']
            character_achievement_points = js['achievement_points']
            character_name = js['name']
            embed=discord.Embed(title=f"", description=f"", color=discord.Color.green())
            embed.set_author(name=f"{character_name}", url=profile_url, icon_url=thumbnail_url)
            embed.set_thumbnail(url=thumbnail_url)
            title = f"Level {character_level} {character_race} {character_class} \n<{character_guild}>\n"
            description = f"[raider.io]({profile_url})\n"
            description += f"[warcraftlogs.com](https://classic.warcraftlogs.com/character/us/mankrik/{character_name})\n"
            embed.add_field(name = title, value = description, inline = False)
            embed.add_field(name = "Item Level", value = character_ilvl_equipped)
            embed.add_field(name = "Achievement Points", value = character_achievement_points, inline = True)
            embed.add_field(name = "Faction", value = character_faction, inline = True)
            embed.add_field(name = "Region", value = character_region, inline = True)
            embed.add_field(name = "Realm", value = character_realm, inline = True)
            embed.add_field(name = "HKs", value = character_honorable_kills, inline = True)
            list_armor = ["head", "neck", "shoulder", "back", "chest", "waist", "wrist", "hands", "legs", "feet"]
            list_jewelry = ["finger1", "finger2"]
            list_trinkets = ["trinket1", "trinket2"]
            list_weapons = ["mainhand", "offhand"]
            list_ranged = ["ranged"]
            armor = ""
            jewelry = ""
            trinkets = ""
            weapons = ""
            ranged = ""
            for key in gear:
                ilvl = str(gear[key]['item_level'])
                id = str(gear[key]['item_id'])
                name = f"[{gear[key]['name']}](https://www.wowhead.com/cata/item={id})"
                desc = "{a} {b}\n".format(
                    a = ilvl,
                    b = name
                )
                if key in list_armor:
                    armor += desc
                if key in list_jewelry:
                    jewelry += desc
                if key in list_trinkets:
                    trinkets += desc
                if key in list_weapons:
                    weapons += desc
                if key in list_ranged:
                    ranged += desc
            embed.add_field(name = "Armor", value = armor, inline = False)
            embed.add_field(name = "Rings", value = jewelry, inline = False)
            embed.add_field(name = "Trinkets", value = trinkets, inline = False)
            embed.add_field(name = "Weapons", value = weapons + ranged, inline = False)
            embed.set_footer(text = f"Profile updated: {character_last_updated}\nGear updated: {character_gear_last_updated}")
            await context.send(embed=embed)

# Cog setup function
async def setup(bot):
    cog = RaiderIO
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
