import os
import logging
import discord
import aiohttp
import io
from PIL import Image
from PIL import ImageSequence
from discord.ext import commands
from includes import config
from includes import logger as log

# Cog class
class ImageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def resize_gif(self, input_path, target_size=(32, 32), keepwidth=False):
        output_path = os.path.join(input_path, input_path.replace('.gif', '_resize.gif'))
        with Image.open(input_path) as gif:
            original_width, original_height = gif.size
            new_width = target_size[0] if not keepwidth else int(target_size[1] * original_width / original_height)
            new_height = int(new_width * original_height / original_width) if not keepwidth else target_size[1]
            new_gif = []
            for i, frame in enumerate(ImageSequence.Iterator(gif)):
                new_frame = frame.copy().convert("RGBA").resize((new_width, new_height))
                new_gif.append(new_frame)
            new_gif[0].save(
                output_path,
                format='GIF',
                save_all = True,
                append_images = new_gif[1:],
                loop = gif.info.get('loop', 0),
                disposal=2
            )
        return output_path

    def resize_image(self, input_path, target_size=(32, 32), keepwidth=True):
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            new_width = target_size[0] if not keepwidth else int(target_size[1] * original_width / original_height)
            new_height = int(new_width * original_height / original_width) if not keepwidth else target_size[1]
            output_path = os.path.join(input_path, input_path + "_resized.png")
            resized_image = img.resize((new_width, new_height))
            resized_image = resized_image.convert("RGBA")
            resized_image.save(output_path, format="PNG")
            return output_path
            
    def is_gif(self, image_path):
        with Image.open(image_path) as img:
            return img.format == 'GIF' and getattr(img, "is_animated", False)
    
    async def download_attachment(self, attachment):
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                if response.status == 200:
                    file_path = os.path.join(config.DIR_DOWNLOADS, attachment.filename)
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    return file_path

    @commands.command(name='icon')
    async def icon(self, ctx):
        """
        Resize the image or gif to a 32x32 icon
        """
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                file = await self.download_attachment(attachment)
                if self.is_gif(file):
                    resized_img = self.resize_gif(file, (32,32), keepwidth=True)
                else:
                    resized_img = self.resize_image(file, (32,32), keepwidth=True)
                await ctx.message.reply(file=discord.File(resized_img))

    @commands.command(name='resize')
    async def resize(self, ctx, width:str, height:str, keepwidth):
        """
        Resize the image or gif
        Arguments: width: int, height: int, 'keepwidth'
        """
        w = int(width)
        h = int(height)
        check_keepwidth = lambda keepwidth: 'keepwidth' in keepwidth
        if not (4 <= int(w) <= 3840) or not (4 <= int(h) <= 3840):
            await ctx.reply("Command requires width and height parameters. (max: 3840x3840)\nresize 128 128")
        if ctx.message.attachments:
            files = []
            for attachment in ctx.message.attachments:
                file = await self.download_attachment(attachment)
                if self.is_gif(file):
                    resized_img = self.resize_gif(file, (w,h), check_keepwidth)
                else:
                    resized_img = self.resize_image(file, (w,h), check_keepwidth)
                await ctx.message.reply(file=discord.File(resized_img))

# Cog setup function
async def setup(bot):
    cog = ImageEdit
    try:
        await bot.add_cog(cog(bot))
        log.log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log.log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
