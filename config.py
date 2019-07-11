#!/usr/bin/env python3
"""Config file for validating .env variables and putting them into objects."""
import os
import json
from models.verify_ip import is_valid_ipv4_address



def max_position():
    user_input = os.environ.get('MAXIMUM_POSITION', None)
    verified_input = user_input
    return verified_input


def path_user_settings():
    user_input = os.environ.get('USER_CONFIG', None)
    verified_input = user_input
    return verified_input

  #  "ip_address": "192.168.0.155",
  #  "default_requested_position": 50000,
  #  "speed": 20000,
  #  "speed_out": 20000
def load_settings():
    settings = dict()
    path = path_user_settings()
    if os.path.isfile(path):
        with open(path) as json_file:
            user_settings = json.load(json_file)
            for k,v in user_settings.items():
                print(type(k),v)
                if k == "ip_address":
                    is_ip = is_valid_ipv4_address(v)
                    print(is_ip)
                    if is_ip == True:
                        settings.update(k,v)
                    else:
                        raise AttributeError("Invalid IP address. ", v, " is not a valid IPv4 address.")
    else:
        raise FileNotFoundError("No settings file found. Using default settings. Missing file ", path)
    return settings







def db_password():
    user_input = os.environ.get('DATABASE_PASSWORD', None)
    verified_input = user_input
    return verified_input

# User settings
