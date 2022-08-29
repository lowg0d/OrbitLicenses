import bot.utils.cc as cc
import pymysql

def connect():
    conn = pymysql.connect(
        host=cc.mysql_host,
        user=cc.mysql_user,
        password=cc.mysql_password,
        db=cc.mysql_db
    )
    return conn

def check_connect():
    try:
        pymysql.connect(
            host=cc.mysql_host,
            user=cc.mysql_user,
            password=cc.mysql_password,
            db=cc.mysql_db)
        return True
    except:
        return False

#####################

def sql_store_license(license_, user_, user_id_):
    
    connection = connect()
    fcursor = connection.cursor()
    
    sql = f"INSERT INTO licenses (license, user, user_id) VALUES ('{license_}','{user_}','{user_id_}')"  
    
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
     

        
    
