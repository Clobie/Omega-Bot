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
import json
from secret import token
import math

try:
    if not token.WCL_API_TOKEN:
        print("Your token.py contains no token for WCL.  Exiting.")
        exit()
except ImportError:
    print("wcl api token issue")

raids_list = [
    "Throne of the Four Winds",
    "Blackwing Descent",
    "Bastion of Twilight"
]

boss_raid_lookup = {
    "Al'Akir": "Throne of the Four Winds",
    "Conclave of Wind": "Throne of the Four Winds",
    "Omnotron Defense System": "Blackwing Descent",
    "Magmaw": "Blackwing Descent",
    "Atramedes": "Blackwing Descent",
    "Chimaeron": "Blackwing Descent",
    "Maloriak": "Blackwing Descent",
    "Nefarian's End": "Blackwing Descent",
    "Halfus Wyrmbreaker": "Bastion of Twilight",
    "Theralion and Valiona": "Bastion of Twilight",
    "Ascendant Council": "Bastion of Twilight",
    "Cho'gall": "Bastion of Twilight"
}

class_spec_emoji_lookup = {
    "druid_balance": "<:balance:1260314861301403740>",
    "druid_feral": "<:feral:1260314909011480586>",
    "druid_guardian": "<:guardian:1260314925331517632>",
    "druid_restoration": "<:restoration:1260314941446164594>",
    "hunter_beastmastery": "<:beastmastery:1260314862572011520>",
    "hunter_marksman": "<:marksman:1260314927340585032>",
    "hunter_survival": "<:survival:1260314968746758265>",
    "mage_arcane": "<:arcane:1260314857752887296>",
    "mage_fire": "<:fire:1260314909938552912>",
    "mage_frost": "<:frost:1260314910940987532>",
    "paladin_holy": "<:holy:1260314926392803379>",
    "paladin_protection": "<:protection:1260314940594720924>",
    "paladin_retribution": "<:retribution:1260314942041624668>",
    "priest_discipline": "<:discipline:1260314906297765980>",
    "priest_shadow": "<:shadow:1260314943266357378>",
    "rogue_assassination": "<:assassination:1260314860462407830>",
    "rogue_combat": "<:combat:1260314883241672744>",
    "rogue_subtlety": "<:subtlety:1260314946084929546>",
    "shaman_elemental": "<:elemental:1260314907149209680>",
    "shaman_enhancement": "<:enhancement:1260314908059373749>",
    "warlock_affliction": "<:affliction:1260314856796717056>",
    "warlock_demonology": "<:demonology:1260314884768530675>",
    "warlock_destruction": "<:destruction:1260314885787488297>",
    "warrior_arms": "<:arms:1260314859120099459>",
    "warrior_fury": "<:fury:1260314923913969748>",
    "deathknight_unholy": "<:unholy:1260314969736613962>",
    "deathknight_blood": "<:blood:1260314880699924652>",
    "deathknight_frost": "<:deathknight_frost:1260314884185395321>",
    "priest_holy": "<:priest_holy:1260314929265905754>",
    "warrior_protection": "<:warrior_protection:1260314970596442143>",
    "shaman_restoration": "<:shaman_restoration:1260314986161504387>"
}

parse_number_emoji_lookup = [
    "<:parse_0:1260305321201635328>",
    "<:parse_1:1260305322191491255>",
    "<:parse_2:1260305322988539985>",
    "<:parse_3:1260305323911282739>",
    "<:parse_4:1260305325173772349>",
    "<:parse_5:1260305325601329276>",
    "<:parse_6:1260305354877833306>",
    "<:parse_7:1260305356022611979>",
    "<:parse_8:1260305356593037384>",
    "<:parse_9:1260305357624840343>",
    "<:parse_10:1260305358845644871>",
    "<:parse_11:1260305360271704076>",
    "<:parse_12:1260305387052073013>",
    "<:parse_13:1260305387878482050>",
    "<:parse_14:1260305388754960455>",
    "<:parse_15:1260305389577048225>",
    "<:parse_16:1260305390382485534>",
    "<:parse_17:1260305391426994320>",
    "<:parse_18:1260305427045023814>",
    "<:parse_19:1260305428122828871>",
    "<:parse_20:1260305428697583717>",
    "<:parse_21:1260305430073053278>",
    "<:parse_22:1260305431142731806>",
    "<:parse_23:1260305432132718602>",
    "<:parse_24:1260305453695631390>",
    "<:parse_25:1260305454609993789>",
    "<:parse_26:1260305455394328738>",
    "<:parse_27:1260305456794959912>",
    "<:parse_28:1260305457822564433>",
    "<:parse_29:1260305459168935956>",
    "<:parse_30:1260305488369811467>",
    "<:parse_31:1260305489338830929>",
    "<:parse_32:1260305490454249532>",
    "<:parse_33:1260305491394035772>",
    "<:parse_34:1260305492622971052>",
    "<:parse_35:1260305493629603850>",
    "<:parse_36:1260305507747627150>",
    "<:parse_37:1260305508385165377>",
    "<:parse_38:1260305509576347790>",
    "<:parse_39:1260305510926651423>",
    "<:parse_40:1260305511744540894>",
    "<:parse_41:1260305512868745257>",
    "<:parse_42:1260305535475908630>",
    "<:parse_43:1260305536608632892>",
    "<:parse_44:1260305537761804381>",
    "<:parse_45:1260305538898595912>",
    "<:parse_46:1260305539682795633>",
    "<:parse_47:1260305540459003936>",
    "<:parse_48:1260305549833015326>",
    "<:parse_49:1260305550684459009>",
    "<:parse_50:1260304599047209050>",
    "<:parse_51:1260304599848583298>",
    "<:parse_52:1260304600645505146>",
    "<:parse_53:1260304601589223554>",
    "<:parse_54:1260304602440536134>",
    "<:parse_55:1260304603350700105>",
    "<:parse_56:1260304604176846890>",
    "<:parse_58:1260304606777311303>",
    "<:parse_57:1260304638138257459>",
    "<:parse_59:1260304650276438056>",
    "<:parse_60:1260304731994063011>",
    "<:parse_61:1260304732799500451>",
    "<:parse_62:1260304733705339012>",
    "<:parse_63:1260304734670295040>",
    "<:parse_64:1260304736146686035>",
    "<:parse_65:1260304737400651908>",
    "<:parse_66:1260304792174202981>",
    "<:parse_67:1260304792962465853>",
    "<:parse_68:1260304794149458022>",
    "<:parse_69:1260304795047301130>",
    "<:parse_70:1260304795969785926>",
    "<:parse_71:1260304796829876406>",
    "<:parse_72:1260304846070874174>",
    "<:parse_73:1260304847606120578>",
    "<:parse_74:1260304848646045747>",
    "<:parse_75:1260304849631973436>",
    "<:parse_76:1260304850588270762>",
    "<:parse_77:1260304851615879241>",
    "<:parse_78:1260304877930676275>",
    "<:parse_79:1260304878786580570>",
    "<:parse_80:1260304879595819160>",
    "<:parse_81:1260304880468230338>",
    "<:parse_82:1260304881487581314>",
    "<:parse_83:1260304883022561340>",
    "<:parse_84:1260304912085155943>",
    "<:parse_85:1260304912974090250>",
    "<:parse_86:1260304913779523696>",
    "<:parse_87:1260304914886693006>",
    "<:parse_88:1260304916010897568>",
    "<:parse_89:1260304916950417541>",
    "<:parse_90:1260304946037915648>",
    "<:parse_91:1260304947174572134>",
    "<:parse_92:1260304952832823368>",
    "<:parse_93:1260304953973538971>",
    "<:parse_94:1260304955085164634>",
    "<:parse_95:1260304956355776605>",
    "<:parse_96:1260304980791922799>",
    "<:parse_97:1260304981823586304>",
    "<:parse_98:1260304982645669888>",
    "<:parse_99:1260304983975530566>",
    "<:parse_100:1260305045828796527>"
]

# Cog class
class WCL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Debug / gathering emojis
    async def fetch_all_emojis(self):
        all_emojis = {}
        for guild in self.bot.guilds:
            emojis = guild.emojis
            for emoji in emojis:
                all_emojis[emoji.name] = emoji.id
        return all_emojis
    
    @commands.command(name="emoji_debug")
    async def emoji_debug(self, ctx):
        all_emojis = await self.fetch_all_emojis()
        with open('emojis.txt', 'w', encoding='utf-8') as file:
            for name, emoji_id in all_emojis.items():
                emoji_string = f"<:{name}:{emoji_id}>\n"
                file.write(emoji_string)

        await ctx.send("Emojis written to file `emojis.txt`!")

    def get_ranking(self, api_key, character, realm, region, timeframe):
        api_v1_url = "https://classic.warcraftlogs.com:443/v1/rankings/character/{}/{}/{}?&metric=dps&timeframe={}&api_key={}".format(
            character, realm, region, timeframe, api_key
        )
        #api_v1_url = "https://classic.warcraftlogs.com:443/v1/rankings/character/{}/{}/{}?api_key={}".format(
        #    character, realm, region, api_key
        #)
        data = requests.get(api_v1_url)
        return data.json()

    def generate_template(self):
            data = {}
            for raid in raids_list:
                data[raid] = {}
                for key in boss_raid_lookup:
                    if boss_raid_lookup[key] == raid:
                        data[raid][key] = {}
            return data

    def parse_data(self, input_data, json_data, raid_size, character_name):
        data = input_data
        for entry in json_data:
            if raid_size == entry["size"]:
                mode = "normal" if entry["difficulty"] == 3 else "heroic" if entry["difficulty"] == 4 else "unknown"
                encounter = entry["encounterName"]
                raid = boss_raid_lookup[encounter]
                rank = entry['rank']
                percentile = math.floor(entry['percentile'])
                percentile_emoji = parse_number_emoji_lookup[int(percentile)]
                class_spec_str = "{}_{}".format(entry['class'].replace(' ', ''), entry['spec']).lower()
                specialization_emoji = class_spec_emoji_lookup[class_spec_str]
                data[raid][encounter][mode] = {}
                data[raid][encounter][mode]["percentile"] = percentile
                data[raid][encounter][mode]["difficulty"] = mode
                data[raid][encounter][mode]["spec_emoji"] = specialization_emoji
                data[raid][encounter][mode]["percentile_emoji"] = percentile_emoji
                data[raid][encounter][mode]["rank"] = rank
                data[raid][encounter][mode]["boss"] = encounter
        return data, character_name, "Mankrik"

    def clean_data_by_highest_percentile(self, input_data):
        encounter_dict = {}
        for entry in input_data:
            key = (entry['encounterID'], entry['size'], entry["difficulty"])
            if key not in encounter_dict or entry['percentile'] > encounter_dict[key]['percentile']:
                encounter_dict[key] = entry
        return list(encounter_dict.values())
    
    def generate_embed(self, input_data, name, realm):
        # Sample character data
        character_name = name
        server = realm
        region = "US"

        embed = discord.Embed(title="Historical Player Rankings", color=0x99aab5)
        embed.add_field(name="Character", value=character_name, inline=True)
        embed.add_field(name="Server", value=server, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        #print(json.dumps(input_data, indent=4))
        for raid_name, bosses in input_data.items():
            #print(raid_name)
            embed.add_field(name=raid_name, value="", inline=False)
            for boss_name, difficulties in bosses.items():
                #print(boss_name)
                spec_emoji = ""
                h_pcnt = ""
                h_rank = ""
                n_pcnt = ""
                n_rank = ""
                for difficulty, stats in difficulties.items():
                    spec_emoji = stats["spec_emoji"]
                    if difficulty == "normal":
                        n_pcnt = stats["percentile_emoji"]
                        n_rank = stats["rank"]
                    else:
                        h_pcnt = stats["percentile_emoji"]
                        h_rank = stats["rank"]
                
                if h_pcnt and n_pcnt:
                    line = "{} Heroic {} (Rank {}) | Normal {} (Rank {}) | {}".format(spec_emoji,h_pcnt,h_rank,n_pcnt,n_rank,boss_name)
                elif n_pcnt:
                    line = "{} Normal {} (Rank {}) | {}".format(spec_emoji,n_pcnt,n_rank,boss_name)
                elif h_pcnt:
                    line = "{} Heroic {} (Rank {}) | {}".format(spec_emoji,h_pcnt,h_rank,boss_name)
                else:
                    line = "No data available - {}".format(boss_name)
                
                embed.add_field(name="", value=line, inline=False)
        embed.set_footer(text="\n\nPowered by Omega\n\n\"Historical\" data shows your highest rank achieved, at the time it was obtained.\n(what WCL shows on your character page by default)\nHowever, you may no longer hold this rank.")
        return embed
    
    @commands.command(name="wcl")
    async def wcl(self, context, character:str, raid_size:int):
        """
        Grabs classic.warcraftlogs.com character data.
        Syntax: wcl <character> <metric> <size>
        """
        async with context.typing():
            # Query the API
            data = self.get_ranking( token.WCL_API_TOKEN, f"{character}", "mankrik", "us", "historical")

            # Error checking
            if "error" in data:
                await context.send(data["error"])
                return

            # Clean up lowest percentiles per boss/size
            data_cleaned = self.clean_data_by_highest_percentile(data)
            #print(data)

            # Generate template
            template = self.generate_template()

            # Parse data
            parsed_data, name, realm = self.parse_data(template, data_cleaned, raid_size, character)

            # Generate embed
            embed = self.generate_embed(parsed_data, name, realm)
            await context.send(embed=embed)
            
# Cog setup function
async def setup(bot):
    cog = WCL
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
