import hikari
from bot import __version__
import bot.managers.config_mg as config

######################

# MSGS
no_permissions_msg = config.get_two("messages", "no_permissions")

#ROLES
owner_role = config.get_two("roles", "owner_id")
user_role = config.get_two("roles", "user_id")

#COLORS
main_color = config.get_two("colors", "main")
correct_color = config.get_two("colors", "correct")
wrong_color = config.get_two("colors", "wrong")
intermediate_color = config.get_two("colors", "intermediate")

#TOKEN
token = config.get("token")

#CONFIG
#logger
debug_enabled = config.get_two("logger","debug")
save_logs_enabled = config.get_two("logger","save-logs")

#mysql
mysql_db = config.get_two("mysql","db")
mysql_host = config.get_two("mysql","host")
mysql_user = config.get_two("mysql","user")
mysql_password = config.get_two("mysql","password")

#channels
logs_channel = config.get_two("channels","logs")

# PRESENCE
default_presence = config.get("default_presence").replace("&version", f"{__version__}")

######################

embed_no_permission = hikari.Embed(title=f"{no_permissions_msg}",color=wrong_color)

######################

def clean_sql_syntax(strtoclean):

    filter_1 = str(strtoclean).replace("'", "")
    filter_2 = str(filter_1).replace("((", "")
    filter_3 = str(filter_2).replace(",),)", "")
    
    return filter_3
