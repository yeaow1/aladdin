from discord.ext import commands
from aiohttp import web

import aiohttp_cors


class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.host = None
        self.api = None

    async def status(self, request):
        ping = round(self.bot.latency * 1000)
        return web.json_response(
            {
                "guilds": len(self.bot.guilds),
                "ping": f"{ping}ms",
            }
        )

    async def run(self):
        print("Setting up web app runner...")
        application = web.Application()
        application.router.add_get("/status", self.status)

        all_methods = ["GET", "POST", "PUT", "DELETE"]

        cors = aiohttp_cors.setup(
            application,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    allow_methods=all_methods,
                )
            },
        )

        for route in list(application.router.routes()):
            cors.add(route)

        starter = web.AppRunner(application)
        await starter.setup()

        print("Creating TCPSite...")
        self.api = web.TCPSite(starter, "0.0.0.0", 2222)

        print("Waiting for bot to be ready...")
        await self.bot.wait_until_ready()

        print("Starting API...")
        await self.api.start()

    async def cog_unload(self):
        if self.api:
            print("Stopping API...")
            await self.api.stop()


async def setup(bot: commands.Bot):
    instance = Server(bot)
    await bot.add_cog(instance)
    await bot.loop.create_task(instance.run())
