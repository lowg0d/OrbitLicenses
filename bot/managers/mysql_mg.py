import bot.utils.cc as cc
import pymysql
import bot.managers.logger_mg as logs
from datetime import datetime

def connect():
    conn = pymysql.connect(
        host=cc.mysql_host,
        user=cc.mysql_user,
        password=cc.mysql_password,
        db=cc.mysql_db
    )
    return conn

def create_tables():
    connection = connect()
    fcursor = connection.cursor()

    sql = f"CREATE TABLE licenses (id int AUTO_INCREMENT PRIMARY KEY, user varchar(80), user_id varchar(80), license varchar(100), creation_date varchar(80))"

    try:
        fcursor.execute(sql)
        connection.commit()
    except:
        connection.rollback()

    connection.close()

def check_tables():
    
    connection = connect()
    fcursor = connection.cursor()
    db = cc.mysql_db

    sql = f"SELECT * FROM {db}.licenses"

    try:
        fcursor.execute(sql)
        connection.commit()
        logs.out("Database table exits skipping this step")
        
    except:
        logs.out("Database table dont exit so creating")
        try:
            create_tables()
            logs.out("Database table sucesfully created !")
        except:
            logs.out("Error creating table", "error")
            
    connection.close()

#####################

def sql_store_license(license_, user_, user_id_):
    
    connection = connect()
    fcursor = connection.cursor()

    current_time = datetime.now()
    time = current_time.strftime("%H:%M:%S")

    creation_date = f"{current_time.year}/{current_time.month}/{current_time.day} {time}"
    
    sql = f"INSERT INTO licenses (license, user, user_id, creation_date) VALUES ('{license_}','{user_}','{user_id_}','{creation_date}')"  
    
    try:
        fcursor.execute(sql)
        connection.commit()
    except:
        connection.rollback()
    
    connection.close()

def update_license(license_, user_, user_id_):
    
    connection = connect()
    fcursor = connection.cursor()

    sql = f"UPDATE licenses SET license='{license_}', user='{user_}' WHERE user_id='{user_id_}'"
    
    try:
        fcursor.execute(sql)
        connection.commit()
    except:
        connection.rollback()
    
    connection.close()
 
#####################

def sql_fetch_user_id(user_id):
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"SELECT user FROM licenses WHERE user_id='{user_id}'"

    fcursor.execute(sql)

    if fcursor.fetchall():
        connection.close()
        return True
        
    else:
        return False
    connection.close()

def sql_fetch_license(license_):
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"SELECT user_id FROM licenses WHERE license='{license_}'"

    fcursor.execute(sql)

    if fcursor.fetchall():
        connection.close()
        return True
        
    else:
        return False
    connection.close()

def sql_get_license(user_id):
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"SELECT license FROM licenses WHERE user_id='{user_id}'"

    fcursor.execute(sql)

    try:
        license_ = fcursor.fetchall()
        connection.close()
        return license_ 
        
    except:
        return False

def sql_get_license_id(user_id):
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"SELECT id FROM licenses WHERE user_id='{user_id}'"

    fcursor.execute(sql)

    try:
        license_ = fcursor.fetchall()
        connection.close()
        return license_ 
        
    except:
        return False 

def sql_get_user(user_id):
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"SELECT user FROM licenses WHERE user_id='{user_id}'"

    fcursor.execute(sql)

    try:
        license_ = fcursor.fetchall()
        connection.close()
        return license_ 
        
    except:
        return False 

def sql_get_date(user_id):
    connection = connect()
    fcursor = connection.cursor()

    sql = f"SELECT creation_date FROM licenses WHERE user_id='{user_id}'"

    fcursor.execute(sql)

    try:
        license_ = fcursor.fetchall()
        connection.close()
        return license_

    except:
        return False

def sql_get_user_id_from_license(license_):
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"SELECT user_id FROM licenses WHERE license='{license_}'"

    fcursor.execute(sql)

    try:
        license_ = fcursor.fetchall()
        connection.close()
        return license_ 
        
    except:
        return False 

def sql_get_license_user_list():
    connection = connect()
    fcursor = connection.cursor()

    sql = f"SELECT user_id, creation_date, id FROM {cc.mysql_db}.licenses"

    fcursor.execute(sql)

    try:
        license_ = fcursor.fetchall()
        connection.close()
        return license_

    except:
        return False


#####################

def sql_delete_license(user_id):
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"DELETE FROM licenses WHERE user_id='{user_id}'" 
    
    license_ = sql_get_license(user_id)
    
    try:
        fcursor.execute(sql)
        connection.commit()
    except:
        connection.rollback()
    
    connection.close()
    return license_
     
    
