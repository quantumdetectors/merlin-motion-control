#!/usr/bin/env python3
"""Config file for validating .env variables and putting them into objects."""
import os
import json
from models.verify_ip import is_valid_ipv4_address
from models import verify_env
from models import verify_settings


def software_version():
    key = 'SOFTWARE_VERSION'
    user_input = os.environ.get(key, None)
    try:
        verify_env.import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '0.9'
    return verified_input

def max_position():
    key = 'MAXIMUM_POSITION'
    user_input = int(os.environ.get(key, None))
    try:
        verify_env.import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = 1
    return verified_input

def path_user_settings():
    key = 'USER_CONFIG'
    user_input = os.environ.get(key, None)
    try:
        verify_env.import_check({key:user_input})
        verified_input = user_input
        file_exists = 1
    except FileNotFoundError as e:
        print(e.__class__, "".join(e.args))
        verified_input = user_input
        file_exists = 0
    return [verified_input, file_exists]

def default_ip():
    key = 'IP_ADDRESS'
    user_input = os.environ.get(key, None)
    try:
        verify_env.import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = '1.1.1.1'
    return verified_input

def default_requested_position():
    key = 'DEFAULT_REQUESTED_POSITION'
    user_input = int(os.environ.get(key, None))
    try:
        verify_env.import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = 1
    return verified_input

def default_speed():
    key = 'SPEED'
    user_input = int(os.environ.get(key, None))
    try:
        verify_env.import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = 1
    return verified_input

def default_speed_out():
    key = 'SPEED_OUT'
    user_input = int(os.environ.get(key, None))
    try:
        verify_env.import_check({key:user_input})
        verified_input = user_input
    except TypeError as e:
        print(e.__class__, "".join(e.args))
        verified_input = 1
    return verified_input

def load_default_settings():
    return {"ip_address":default_ip(),
            "default_requested_position":default_requested_position(),
            "speed":default_speed(),
            "speed_out":default_speed_out()
           }

def load_user_settings():
    settings = dict()
    [path,path_exists] = path_user_settings()
    if path_exists == 0:
        settings = load_default_settings()
    else:
        with open(path, 'r') as json_file:
            user_settings = json.load(json_file)
            try:
                verify_settings.import_check(user_settings)
            except TypeError as e:
                print(e.__class__, "".join(e.args))
                user_settings["speed"] = default_speed()
            except BlockingIOError as e:
                print(e.__class__, "".join(e.args))
                user_settings["speed_out"] = default_speed_out()
            except ValueError as e:
                print(e.__class__, "".join(e.args))
                user_settings["default_requested_position"] = default_requested_position()
            except AttributeError as e:
                print(e.__class__, "".join(e.args))
                user_settings["ip_address"] = default_ip()
            finally:
                settings = user_settings

    with open(path, 'w') as json_file:
        json.dump(settings, json_file, indent=2)

    settings["max_position"] = max_position()
    settings["software_version"] = software_version()
    settings["title"] = "Merlin Motion Control"
    return settings


def db_password():
    user_input = os.environ.get('DATABASE_PASSWORD', None)
    verified_input = user_input
    return verified_input
