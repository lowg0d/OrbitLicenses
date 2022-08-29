import os
import sys
import json

##################################################################
# check if config exists, if it exits save it in config_file var

configjson_path = "./bot/config/config.json"

if not os.path.isfile(f'{configjson_path}'):
    sys.exit("'[-] config.json' not found! Please add it and try again.")

else:
    with open(f'{configjson_path}') as file:
        config_file = json.load(file)

##################################################################
# get config functions

def get(parameter):
    try:
        # get the parameter from the config file
        response = config_file[f'{parameter}']
        return response  # resturn the parameter
    except:
        print(f'[-] parameter "{parameter}" not in the config.json')
        exit()

def get_two(parameter1, parameter2):
    try:
        # get the parameters from the config file
        response = config_file[f'{parameter1}'][f'{parameter2}']
        return response  # resturn the parameters
    except:
        print(
            f'[-] parameter "{parameter1}.{parameter2}" not in the config.json')
        exit()

def get_three(parameter1, parameter2, parameter3):
    try:
        # get the parameters from the config file
        response = config_file[f'{parameter1}'][f'{parameter2}'][f'{parameter3}']
        return response  # resturn the parameters
    except:
        print(
            f'[-] parameter "{parameter1}.{parameter2}.{parameter3}" not in the config.json')
        exit()
