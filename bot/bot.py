import os
import sys
import time
import dotenv
import hikari
import fnmatch
import aiohttp
import asyncio
import lightbulb
import bot.utils.cc as cc
from bot import __version__
import bot.managers.logger_mg as logs
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
            
            try:
                sql_mg.connect()
                logs.out("Sucesfully connected to the database")
            except:
                logs.out("Error connecting to the database")
                sys.exit()
            sql_mg.check_tables()

                
        # stop aio session
        @self.bot.listen()
        async def on_stopping(event: hikari.StoppingEvent) -> None:
            await self.bot.aio_session.close()
            sys.exit()
        
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
