import discord
from discord import *
from discord.ext import *
from models import Levels as LevelDB
import random
import asyncio
from typing import *
import easy_pil


class Level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        author = message.author
        guild = message.guild
        required_level: int = 100
        messages = {}

        level_db: LevelDB = await LevelDB.filter(user_id=author.id, guild_id=guild.id).get_or_none()
        if not level_db:
            new_level_values = await LevelDB.create(
                user_id=author.id, guild_id=guild.id, xp=0, level=0
            )
            

        xp = level_db.xp if level_db else 0
        level = level_db.level if level_db else 0

        if level < 5:
            xp += random.randint(1, 10)
            level_db.xp = xp
            await level_db.save()
        else:
            level_xp_base = random.randint(1, (level // 4))
            if level_xp_base == 1:
                xp += random.randint(1, 5)
                level_db.xp = xp
                await level_db.save()

        if xp >= required_level:
            level += 1
            await level_db.filter(user_id=author.id, guild_id=guild.id).update(
                level=level, xp=0
            )
            
            return await message.channel.send(
                f"**Congratulations {author.mention}! You leveled up to level {level}!**", silent=True
            )

    @app_commands.command(name="level", description="View your/someone level card.")
    async def level(
        self, interaction: discord.Interaction, user: Optional[discord.Member] = None
    ):
        await interaction.response.defer()

        if user is None:
            user = interaction.user

        level_db: LevelDB = await LevelDB.filter(user_id=user.id,  guild_id=user.guild.id).get_or_none()

        if not level_db:
            return await interaction.followup.send(
                f"This user don't have any level yet", ephemeral=True
            )

        username = f"{user.global_name} ({user.name})"
        exp = level_db.xp
        level = level_db.level
        required_level = 100
        percent = level_db.xp

        bg = easy_pil.Editor(easy_pil.Canvas((900, 300), color="#1c1c1c"))
        picture = await easy_pil.load_image_async(str(user.avatar.url))
        profile = easy_pil.Editor(picture).resize((150, 150)).circle_image()
        profile_with_border = easy_pil.Editor(easy_pil.Canvas((160, 160), color="#FFFFFF"))
        profile_with_border.paste(profile, (5,5)).circle_image()

        poppins = easy_pil.Font.poppins(size=40)
        poppins_small = easy_pil.Font.poppins(size=30)

        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

        bg.polygon(card_right_shape, color="#0096FF")
        bg.paste(profile_with_border, (30, 30))
        bg.rectangle((30, 220), width=650, height=40, color="#0096FF", radius=20)
        bg.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percent,
            color="#FFFFFF",
            radius=20,
        )
        bg.text((200, 40), username, font=poppins, color="#FFFFFF")

        bg.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
        bg.text(
            (200, 130),
            f"Level {level} - EXP {exp}/{required_level}",
            font=poppins_small,
            color="#FFFFFF",
        )

        file = discord.File(fp=bg.image_bytes, filename="level.png")

        await asyncio.sleep(5)
        return await interaction.followup.send(file=file, silent=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Level(bot))
