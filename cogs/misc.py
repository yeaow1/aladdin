import discord
from discord import app_commands
from discord.ext import commands
import requests


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Get IP details.")
    async def ip(self, interaction: discord.Interaction, address: str):
        response = requests.get(f"http://ip-api.com/json/{address}")
        data = response.json()
        if response.status_code == 200:
            embed = discord.Embed(
                title="IP Lookup", description=f"All details for the IP `{address}`"
            )
            file_path = "images/aladdin-ip.gif"
            file = discord.File(file_path, "aladdin-ip.gif")
            embed.set_thumbnail(url="attachment://aladdin-ip.gif")

            embed.add_field(name="Country", value=data["country"])
            embed.add_field(name="Code", value=data["countryCode"])
            embed.add_field(name="Region", value=data["region"])
            embed.add_field(name="Region Name", value=data["regionName"])
            embed.add_field(name="City", value=data["city"])
            embed.add_field(name="Zip", value=data["zip"])
            embed.add_field(name="Lat.", value=data["lat"])
            embed.add_field(name="Lon.", value=data["lon"])
            embed.add_field(name="Timezone", value=data["timezone"])

            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(
                f"Error trying to fetch the info about {address}."
            )


async def setup(bot):
    await bot.add_cog(Misc(bot))
