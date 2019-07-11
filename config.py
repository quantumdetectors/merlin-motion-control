#!/usr/bin/env python3
"""Config file for validating .env variables and putting them into objects."""
import os
import json
from models.verify_ip import is_valid_ipv4_address


def software_version():
    user_input = os.environ.get('SOFTWARE_VERSION', None)
    verified_input = user_input
    return verified_input

def max_position():
    user_input = os.environ.get('MAXIMUM_POSITION', None)
    verified_input = user_input
    return verified_input

def path_user_settings():
    user_input = os.environ.get('USER_CONFIG', None)
    verified_input = user_input
    return verified_input

def default_ip():
    user_input = os.environ.get('IP_ADDRESS', None)
    verified_input = user_input
    return verified_input

def default_requested_position():
    user_input = os.environ.get('DEFAULT_REQUESTED_POSITION', None)
    verified_input = user_input
    return verified_input

def default_speed():
    user_input = os.environ.get('SPEED', None)
    verified_input = user_input
    return verified_input

def default_speed_out():
    user_input = os.environ.get('SPEED_OUT', None)
    verified_input = user_input
    return verified_input

def load_user_settings():
    settings = dict()
    path = path_user_settings()
    if os.path.isfile(path):
        with open(path) as json_file:
            user_settings = json.load(json_file)
            for k,v in user_settings.items():
                if k == "ip_address":
                    is_ip = is_valid_ipv4_address(v)
                    print(is_ip)
                    if is_ip == True:
                        settings.update({k:v})
                    else:
                        raise AttributeError("Invalid IP address. ", v, " is not a valid IPv4 address.")
                elif isinstance(v,int):
                    settings.update({k:v})
                else:
                    raise AttributeError("Invalid type. ", k," requires an integer value but has been set to ", v, ".")
    else:
        raise FileNotFoundError("No settings file found. Using default settings. Missing file ", path)
    return settings


def db_password():
    user_input = os.environ.get('DATABASE_PASSWORD', None)
    verified_input = user_input
    return verified_input

# User settings
