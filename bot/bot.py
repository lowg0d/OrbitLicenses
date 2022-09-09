"""
ORBIT LICENSES
"""
import os
import sys
import time
import dotenv
import hikari
import fnmatch
import aiohttp
import asyncio
import lightbulb
import bot
import bot.utils.cc as cc
from bot import __version__
import bot.managers.mysql_mg as sql_mg

########################
extension_path = "./bot/extensions"
########################

class Bot:
    def __init__(self):
        global globalbot
        
        self.token = cc.token
        dotenv.load_dotenv()
        
        self.bot = lightbulb.BotApp(
            token=self.token,
            intents=hikari.Intents.ALL_UNPRIVILEGED)
        
        globalbot = self.bot
        
    def start(self):
        
        # load extensions
        self.load_extensions()
        
        # start aio session
        @self.bot.listen()
        async def on_starting(event: hikari.StartingEvent) -> None:
            self.bot.d.aio_session = aiohttp.ClientSession()
            
            embed_message = hikari.Embed(
                                title=f"OrbitLicenses v{__version__}",
                                description=f"Bot Sucesfully Started\n>>> MySql connection: :green_circle:",
                                color=cc.main_color)
            embed_message.set_footer(f"OrbitLicenses v{__version__} - by @lowg0d#9605")
            
            #await self.bot.rest.create_message(1002591521087946752, embed_message)
                
        # stop aio session
        @self.bot.listen()
        async def on_stopping(event: hikari.StoppingEvent) -> None:
            await self.bot.aio_session.close()
        
        # run the bot
        self.bot.run(activity=hikari.Activity(
                    name=cc.default_presence,
                    type=hikari.ActivityType.WATCHING), 
                    asyncio_debug=True,
                    coroutine_tracking_depth=20,
                    propagate_interrupts=True)
        
    
    def load_extensions(self):
        
        extension_path_nodots = extension_path.replace('./', "")
        
        for f in os.listdir(extension_path):
            if fnmatch.fnmatch(f, '*.py'):
                time.sleep(0.2)
                extension = f.replace('.py', '')
                self.bot.load_extensions(f"{extension_path_nodots.replace('/', '.')}.{extension}")
