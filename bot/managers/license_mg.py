import bot.utils.keygenerator as keygen
import bot.managers.mysql_mg as sql_mg

#####################

# check if user in on the database 
def check_if_user_on_db(user_id):
    # try to find the user in the database
    if sql_mg.sql_fetch_user_id(user_id) == True:
        return True
    else:
        return False

#####################

# generate license function
def generate_new_license(user_id, user):

    # generate new license
    new_license = keygen.gen_license()
    while sql_mg.sql_fetch_license(new_license) == True:
        new_license = keygen.gen_license()
    
    # store the license in the database
    sql_mg.sql_store_license(f"{new_license}", f"{user}", f"{user_id}")
    
    return new_license
    
