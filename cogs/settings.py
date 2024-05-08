import discord
from discord import app_commands
from discord.ext import commands
from models import GuildSettings, WelcomeSettings, LeaveSettings
import typing
import os


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(
        name="setprefix", description="Set a new prefix for the server"
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def setprefix(
        self,
        interaction: discord.Interaction,
        *,
        prefix: typing.Optional[str] = None,
    ):
        current_guild_id = interaction.guild_id

        guild_settings = await GuildSettings.filter(
            guild_id=current_guild_id
        ).get_or_none()
        if not prefix:
            current_prefix = (
                guild_settings.guild_prefix
                if guild_settings
                else os.environ["DEFAULT_PREFIX"]
            )
            embed1 = discord.Embed(
                description=f"The current command prefix on this server is set to `{current_prefix}`"
            )
            # embed1.set_author(icon_url=self.bot.user.display_avatar, name=self.bot.user)
            # embed1.set_thumbnail(url=self.bot.user.display_avatar)
            return await interaction.response.send_message(embed=embed1)
        if not guild_settings:
            new_guild_settings = await GuildSettings(
                guild_id=current_guild_id, guild_prefix=prefix
            )
            await new_guild_settings.save()
        else:
            guild_settings.guild_prefix = prefix
            await guild_settings.save()

        embed2 = discord.Embed(
            description=f"The new prefix defined for this server is now `{prefix}`"
        )
        embed2.set_author(icon_url=self.bot.user.display_avatar, name=self.bot.user)
        embed2.set_thumbnail(url=self.bot.user.display_avatar)
        return await interaction.response.send_message(embed=embed2)

    @app_commands.command(name="welcome", description="Welcome")
    @commands.has_guild_permissions(manage_guild=True)
    async def welcome(self, interaction: discord.Interaction):
        settings = await GuildSettings.filter(
            guild_id=interaction.guild_id
        ).get_or_none()
        welcome = await WelcomeSettings.filter(
            guild_id=interaction.guild_id
        ).get_or_none()
        if settings.welcome_enabled:
            channel = discord.utils.get(
                interaction.guild.channels, id=welcome.channel_id
            )
            return await interaction.response.send_message(
                f"Welcome messages are enabled for this server in the channel {channel.mention}"
            )
        else:
            return await interaction.response.send_message(
                f"Welcome messages are not enabled for this server, check your dashboard settings."
            )

    @app_commands.command(name="leave", description="Leave")
    @commands.has_guild_permissions(manage_guild=True)
    async def leave(self, interaction: discord.Interaction):
        settings = await GuildSettings.filter(
            guild_id=interaction.guild_id
        ).get_or_none()
        leave = await LeaveSettings.filter(guild_id=interaction.guild_id).get_or_none()
        if settings.leave_enabled:
            channel = discord.utils.get(interaction.guild.channels, id=leave.channel_id)
            return await interaction.response.send_message(
                f"Leave messages are enabled for this server in the channel {channel.mention}"
            )
        else:
            return await interaction.response.send_message(
                f"Leave messages are not enabled for this server, check your dashboard settings."
            )

    @app_commands.command(
        name="setwelcome", description="Set a message for new members"
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def setwelcome(
        self,
        interaction: discord.Interaction,
        *,
        message: typing.Optional[str] = None,
        channel: discord.TextChannel,
    ):
        await interaction.response.defer()
        guild_settings = await GuildSettings.filter(
            guild_id=interaction.guild_id
        ).get_or_none()
        welcome_settings = await WelcomeSettings.filter(
            guild_id=interaction.guild_id
        ).get_or_none()
        try:
            guild_settings.welcome_enabled = True
            await guild_settings.save()
            if not welcome_settings:
                new_welcome_settings = await WelcomeSettings(
                    guild_id=interaction.guild_id,
                    channel_id=channel.id,
                    welcome_message=message,
                )
                await new_welcome_settings.save()
                return await interaction.followup.send(
                    f"Channel to received welcome message event: `{channel.name}`"
                )
            else:
                welcome_settings.channel_id = channel.id
                welcome_settings.welcome_message = message
                await welcome_settings.save()
                return await interaction.followup.send(
                    f"Welcome settings has been updated in database, new channel welcome events: `{channel.name}`"
                )

        except commands.errors.ChannelNotFound as channel_error:
            embed = discord.Embed(description=f"Invalid channel {channel_error}")
            return await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="setleave",
        description="Set a message for members that would leave your guild",
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def setleave(
        self,
        interaction: discord.Interaction,
        *,
        message: typing.Optional[str] = None,
        channel: discord.TextChannel,
    ):
        await interaction.response.defer()
        guild_settings = await GuildSettings.filter(
            guild_id=interaction.guild_id
        ).get_or_none()
        leave_settings = await LeaveSettings.filter(
            guild_id=interaction.guild_id
        ).get_or_none()
        try:
            guild_settings.leave_enabled = True
            await guild_settings.save()
            if not leave_settings:
                new_leave_settings = await LeaveSettings(
                    guild_id=interaction.guild_id,
                    channel_id=channel.id,
                    leave_message=message,
                )
                await new_leave_settings.save()
                return await interaction.followup.send(
                    f"Channel to received leave message event: `{channel.name}`"
                )
            else:
                leave_settings.channel_id = channel.id
                leave_settings.leave_message = message
                await leave_settings.save()
                return await interaction.followup.send(
                    f"Welcome settings has been updated in database, new channel welcome events: `{channel.name}`"
                )

        except commands.errors.ChannelNotFound as channel_error:
            embed = discord.Embed(description=f"Invalid channel {channel_error}")
            return await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))
