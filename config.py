#!/usr/bin/env python3
"""Config file for validating .env variables and putting them into objects."""
import os
import json
from models.verify_ip import is_valid_ipv4_address
from models.verify_env import import_check


def software_version():
    key = 'SOFTWARE_VERSION'
    user_input = os.environ.get(key, None)
    try:
        import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '0.9'
    return verified_input

def max_position():
    key = 'MAXIMUM_POSITION'
    user_input = os.environ.get(key, None)
    try:
        import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '280000'
    return verified_input

def path_user_settings():
    key = 'USER_CONFIG'
    user_input = os.environ.get(key, None)
    try:
        import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = 'settings.json'
    return verified_input

def default_ip():
    key = 'IP_ADDRESS'
    user_input = os.environ.get(key, None)
    try:
        import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '192.168.0.150'
    return verified_input

def default_requested_position():
    key = 'DEFAULT_REQUESTED_POSITION'
    user_input = os.environ.get(key, None)
    try:
        import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '180000'
    return verified_input

def default_speed():
    key = 'SPEED'
    user_input = os.environ.get(key, None)
    try:
        import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '20000'
    return verified_input

def default_speed_out():
    key = 'SPEED_OUT'
    user_input = os.environ.get(key, None)
    try:
        import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '20000'
    return verified_input

def load_user_settings():
    settings = dict()
    path = path_user_settings()
    if os.path.isfile(path):
        with open(path) as json_file:
            user_settings = json.load(json_file)
            for k,v in user_settings.items():
                if k == "ip_address":
                    if is_valid_ipv4_address(v):
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
