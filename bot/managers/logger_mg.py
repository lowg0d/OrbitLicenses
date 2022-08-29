"""
Python Logger script
--------------------
version: V2.0
date: 26.4.22
author: lowg0d_
"""
import os
import pytz
from rich import print
from datetime import datetime
import bot.utils.cc as cc
import bot.managers.config_mg as config
##################################################################


# Your time zone or the time zone you want the logs to have.
TIME_ZONE = 'Europe/Madrid'
# If you select true in the above option u can edit the name of the folder.
LOG_FOLDER_NAME = "logs"

DEBUG = cc.debug_enabled 
# config.get_config("save_flight_logs") # Select True if you want your logs to save in a folder on the script directory.
SAVE_LOGS = cc.save_logs_enabled 

# log prefix "[EXAMPLE] Lorem ipsum"
DEBUG_PREFIX = 'DEBUG'
INFO_PREFIX = 'INFO'
WARN_PREFIX = 'WARN'
ERROR_PREFIX = 'ERROR'
CRITICAL_PREFIX = 'CRITICAL'

ERROR_COLOR = "red"
INFO_COLOR = "green"
WARNING_COLOR = "orange"

##################################################################

# time formats
date_format = "%d.%m.%y"
time_format = "%H:%M:%S"
time_format_folder = "%H.%M.%S"

# the time of the moment when the log have been created.
log_date = datetime.now(pytz.timezone(TIME_ZONE)).strftime(date_format)
log_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime(time_format_folder)

global f

# if the option to save logs is activated.
if SAVE_LOGS:
    # the name of the new log file.
    log_name = f"log-{log_date}-{log_time}.txt"
    # create the file
    try:
        # if the directory to save the logs doesen't, this is responsible for creating it.
        if not os.path.exists(f"{LOG_FOLDER_NAME}"):
            os.makedirs(f"{LOG_FOLDER_NAME}")
        # create the log file
        f = open(f"{LOG_FOLDER_NAME}/{log_name}", 'w')
        f.write(
            f"LOG DATE: {log_date} | LOG_TIME: {log_time}\n---------------------------------------------------------------\n")
    except:
        raise Exception("Error creating the log folder")

# this function is used to detect what kind of log you wanna use.


def detec_log_lvl(lvl):
    if lvl.lower() == "debug":
        return DEBUG_PREFIX
    elif lvl.lower() == "info":
        return INFO_PREFIX
    elif lvl.lower() == "warn":
        return WARN_PREFIX
    elif lvl.lower() == "error":
        return ERROR_PREFIX
    elif lvl.lower() == "critical":
        return CRITICAL_PREFIX
    else:
        raise ValueError(f"wrong log level: {lvl}")

# this function is used to detect what kind of log you wanna use.


def detec_log_color(lvl):
    if lvl.lower() == "debug":
        return "[cornflower_blue]"
    elif lvl.lower() == "info":
        return "[bright_green]"
    elif lvl.lower() == "warn":
        return "[orange1]"
    elif lvl.lower() == "error":
        return "[dark_red]"
    elif lvl.lower() == "critical":
        return "[bright_red]"
    else:
        raise ValueError(f"wrong log level: {lvl}")

# this is the main function, writes the logs on the console and also can write the logs on a file if you put the SAVE_LOGS option True.


def out(msg="Default log msg", lvl="info", prefix=""):
    # the time of the log
    log_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime(time_format)

    # if the custom prefix is nonexistent, automatically set to nothing.
    if len(str(prefix)) <= 0:
        prefix = ""
    else:
        prefix = f"({prefix}) "

    # detect what level you wanna use to this specific log.
    log_lvl = detec_log_lvl(lvl)

    # detect what level you wanna use to this specific log.
    log_color = detec_log_color(lvl)

    # the outpur format.
    output_format = f"{log_color}[{log_time} {log_lvl}]: {prefix}{msg}"
    save_format = f"[{log_time} {log_lvl}]: {prefix}{msg}"

    if lvl == "debug":
        if DEBUG == True:
            print(output_format)
        else:
            pass

    elif lvl != "debug":
        # print the log on the console.
        print(output_format)

    # if SAVE_LOGS is activated also write the log on the file.
    if SAVE_LOGS:
        f.write(save_format + "\n")


def out_silence(msg="Default log msg", lvl="info", prefix=""):
    # the time of the log
    log_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime(time_format)

    # if the custom prefix is nonexistent, automatically set to nothing.
    if len(str(prefix)) <= 0:
        prefix = ""
    else:
        prefix = f"({prefix}) "

    # detect what level you wanna use to this specific log.
    log_lvl = detec_log_lvl(lvl)

    save_format = f"[{log_time} {log_lvl}]: {prefix}{msg}"

    # print the log on the console.

    # if SAVE_LOGS is activated also write the log on the file.
    if SAVE_LOGS:
        f.write(save_format + "\n")
    else:
        pass
