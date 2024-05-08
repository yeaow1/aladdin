# All imports
import discord
from discord.ext import commands
import os
from database import database_connection
from dotenv import load_dotenv
from models import GuildSettings, WelcomeSettings, LeaveSettings
import wavelink

load_dotenv()

permissions = discord.Intents.all()

async def load_prefix(bot: commands.Bot, message: discord.Message):
    config = await GuildSettings.filter(guild_id=message.guild.id).get_or_none()
    return config.guild_prefix if config else os.environ["DEFAULT_PREFIX"]

bot = commands.Bot(command_prefix=load_prefix, intents=permissions)

@bot.event
async def on_guild_join(guild: discord.Guild):
    new_config = await GuildSettings(guild_id=guild.id, guild_name=guild.name)
    await new_config.save()

@bot.event
async def on_member_join(member: discord.Member):

    settings = await GuildSettings.filter(guild_id=member.guild.id).get_or_none()
    if not settings:
        return

    if settings.welcome_enabled:
        welcome = await WelcomeSettings.filter(guild_id=member.guild.id).get_or_none()
        embed = discord.Embed(
            title="Welcome to our server!", description=welcome.welcome_message
        )
        embed.set_author(icon_url=member.avatar, name=member.name)

        channel_to_send_message = discord.utils.get(
            member.guild.channels, id=welcome.channel_id
        )
        return await channel_to_send_message.send(embed=embed)

@bot.event
async def on_member_remove(member: discord.Member):
    
    settings = await GuildSettings.filter(guild_id=member.guild.id).get_or_none()
    if not settings:
        return

    if settings.leave_enabled:
        welcome = await Leave.filter(guild_id=member.guild.id).get_or_none()
        embed = discord.Embed(
            title=f"Bye bye {member.name}", description=leave.leave_message
        )
        embed.set_author(icon_url=member.avatar, name=member.name)

        channel_to_send_message = discord.utils.get(
            member.guild.channels, id=leave.channel_id
        )
        return await channel_to_send_message.send(embed=embed)

async def load_all_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

@bot.event
async def on_ready():
    await load_all_cogs()
    await bot.tree.sync()
    await database_connection()
    guilds = len(bot.guilds)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, name=f"on {guilds} servers"
        )
    )
    print(f"{bot.user} has been initialized!")

bot.run(os.environ["DISCORD_BOT_TOKEN"], reconnect=True)