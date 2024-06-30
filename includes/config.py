import os

# Bot settings
BOT_PREFIX = '.'
main_color = 0xD75BF4
error = 0xE02B2B
success = 0x42F56C
warning = 0xF59E42
info = 0x4299F5

# Directory structure
CWD = os.getcwd()
DIR_INCLUDES = os.path.join(CWD, "includes")
DIR_LOGS = os.path.join(CWD, "logs")
DIR_COGS = os.path.join(CWD, "cogs")
DIR_DOWNLOADS = os.path.join(CWD, "downloads")
DIR_ASSETS = os.path.join(CWD, "assets")
DIR_SCRIPTS = os.path.join(CWD, "scripts")

os.makedirs(DIR_LOGS, exist_ok=True)
os.makedirs(DIR_DOWNLOADS, exist_ok=True)

# Reused assets
THINKING_GIF = DIR_ASSETS = os.path.join(DIR_ASSETS, "bubble-loading.gif")