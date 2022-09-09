import hikari
from bot import __version__
import bot.managers.config_mg as config

######################

# MSGS
no_permissions_msg = config.get_two("messages", "no_permissions")

you_own_license_msg = config.get_two("messages", "you_own_license")
user_own_license_msg = config.get_two("messages", "user_own_license")
sucesfully_generated_license_msg = config.get_two("messages", "sucesfully_generated_license")
sucesfully_generated_license_for_msg = config.get_two("messages", "sucesfully_generated_license_for")
sucesfully_deleted_license_msg = config.get_two("messages", "sucesfully_deleted_license")
sucesfully_regenerated_msg = config.get_two("messages", "sucesfully_regenerated")
user_not_license_registered_msg = config.get_two("messages", "user_not_license_registered")

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

    filter_0 = str(strtoclean).replace("'", "")
    filter_1 = str(filter_0).replace("(", "")
    filter_2 = str(filter_1).replace("((", "")
    filter_3 = str(filter_2).replace(",),)", "")
    filter_4 = str(filter_3).replace("(", "")
    filter_5 = str(filter_4).replace(",)", "")
    
    return filter_5
