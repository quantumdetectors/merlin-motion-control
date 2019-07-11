#!/usr/bin/env python3
"""Config file for validating .env variables and putting them into objects."""
import os
import json
from models import verify_ip



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
    if os.path.isfile(path_user_settings()):
        with open(path_user_settings()) as json_file:
            user_settings = json.load(json_file)
            for k,v in user_settings.items():
                print(k,v)
                if k is "ip_address":
                    is_ip = verify_ip(v)
                    if is_ip == True:
                        continue
                    else:
                        raise "Invalid IP address"






def db_password():
    user_input = os.environ.get('DATABASE_PASSWORD', None)
    verified_input = user_input
    return verified_input

# User settings
