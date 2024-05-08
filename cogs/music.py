import discord
from discord.ext import commands
from discord import app_commands
import wavelink
import asyncio

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot, host="54.36.225.156", port=2334, password="s4DarqP$&y"
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready.")
        
    @app_commands.command(name="play", description="Play a song.")
    async def play(self, interaction: discord.Interaction, query: str):
        
        search = await wavelink.YouTubeTrack.search(query=query, return_first=True)

        if search:
            embed = discord.Embed(color=0x3498db)
            if not interaction.guild.voice_client:
                # Se o bot não estiver em um canal de voz, ele se conecta
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
            else:
                # Se já estiver em um canal, usa o mesmo player
                vc: wavelink.Player = interaction.guild.voice_client

            await vc.play(search)
            await interaction.response.send_message(f"Playing now `{search.title}`")
        else:
            await interaction.response.send_message("No music found for the given query.")

    @app_commands.command(name="pause", description="Pause a song.")
    async def pause(self, interaction: discord.Interaction):
        if interaction.response.is_done():
            return
        
        await interaction.response.defer()

        embed = discord.Embed(color=0x3498db)
        vc: wavelink.Player = await interaction.guild.voice_client
        if vc:
            embed.description = "The song has been paused."
            await vc.pause()
            return await interaction.followup.send(embed=embed, silent=True)
        else:
            embed.description = "I'm not currently in a voice channel to pause."
            return await interaction.followup.send(embed=embed, silent=True)

    @app_commands.command(name="dc", description="Disconnect the bot from voice channel.")
    async def dc(self, interaction: discord.Interaction):
        embed = discord.Embed(color=0x3498db)

        vc = interaction.guild.voice_client
        if vc:
            embed.description = "I have been kicked from the voice channel 😔"
        else:
            embed.description = "I'm not currently in a voice channel."
            
        await vc.disconnect()
        await interaction.response.send_message(embed=embed, silent=True)



async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))