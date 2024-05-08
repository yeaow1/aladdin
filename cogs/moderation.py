import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import datetime
import humanfriendly


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(
        name="ban", description="Ban a specific user from the server."
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: Optional[str],
    ):
        if not reason:
            reason = "No reason."
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                description=f"A team member kicked the user: `{member}`\n Ban Reason: `{reason}`",
            )

            embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
            await interaction.response.send_message(embed=embed)
        except:
            error = await self.bot.error(f"I'm not able to ban the user {member}.")
            await interaction.response.send_message(error)

    @app_commands.command(
        name="kick", description="Kick a specific user from the server."
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: Optional[str],
    ):
        if not reason:
            reason = "No reason."
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                description=f"A team member kicked the user: `{member}`\n Kick Reason: `{reason}`",
            )
            embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
            await interaction.response.send_message(embed=embed)
        except:
            error = await self.bot.error(f"I'm not able to kick the user {member}.")
            await interaction.response.send_message(error)

    @app_commands.command(name="purge", description="Clear messages.")
    @commands.has_guild_permissions(manage_guild=True)
    async def purge(self, interaction: discord.Interaction, amount: Optional[int] = 10):
        channel_name = interaction.channel.mention
        await interaction.response.defer(ephemeral=True)

        if amount > 100:
            await interaction.followup.send(
                f"{interaction.user.mention} You exceeded the maximum limit for the amount messages to purge."
            )
            return

        deleted_messages = await interaction.channel.purge(
            limit=amount - 1 if amount > 1 else 1
        )

        return await interaction.followup.send(
            f"Total of {len(deleted_messages)} messages has been cleaned on {channel_name}."
        )

    @app_commands.command(name="mute", description="Mute a user.")
    @commands.has_guild_permissions(manage_guild=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        time: str,
        *,
        reason: Optional[str],
    ):
        if not reason:
            reason = "No reason."

        embed = discord.Embed()

        time = humanfriendly.parse_timespan(time)
        timeout = discord.utils.utcnow() + datetime.timedelta(seconds=time)

        timeout_to_string = f"{timeout:%Y-%m-%d %H:%M:%S}"

        await member.edit(timed_out_until=timeout)
        embed.description = (
            f"{member.mention} has been muted until `{timeout_to_string}`."
        )

        return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute", description="Unmute a user.")
    @commands.has_guild_permissions(manage_guild=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed()
        await member.edit(timed_out_until=None)
        embed.description = f"The user {member.mention} has been unmuted."
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
