#!/usr/bin/python
import os
import asyncio
from bot.bot import Bot
from bot import __version__
import bot.managers.logger_mg as logs

if __name__ == '__main__':
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        os.system('cls')
    else:    
        os.system('clear')
        
    logs.out(f"Starting OrbitLicenses v{__version__}")
    ######################

    botapp = Bot()
    botapp.start()
