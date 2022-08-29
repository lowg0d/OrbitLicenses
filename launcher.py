#!/usr/bin/python
import os
import sys
import asyncio
from bot.bot import Bot
from bot import __version__
import bot.managers.logger_mg as logs
import bot.managers.mysql_mg as sql_mg

if __name__ == '__main__':
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        os.system('cls')
    else:    
        os.system('clear')
        
    logs.out(f"Starting OrbitLicenses Bot v{__version__}")
    ######################

    logs.out(f"Attempting Connection to the database")
    
    """"
    try:
        sql_mg.connect()
        logs.out(f"Sucesfully connected to the database.")
    except:
        logs.out("Error connecting to the MySQL server, check the database status and try again.", "error")
        sys.exit()
    
    logs.out(f"Starting the bot.")
    os.system('cls')
    """
    botapp = Bot()
    botapp.start()
