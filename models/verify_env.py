MAXIMUM_POSITION=50000
USER_CONFIG=settings.json
IP_ADDRESS=192.168.0.10
DEFAULT_REQUESTED_POSITION=50000
SPEED=20000
SPEED_OUT=20000
SOFTWARE_VERSION=0.1
from models.verify_ip import is_valid_ipv4_address
import os


def import_check(settings):
    if isinstance(settings,dict):

        if not settings["MAXIMUM_POSITION"] and\
          not isinstance(settings["MAXIMUM_POSITION"], int) and\
          not settings["MAXIMUM_POSITION"] > 0:
            raise TypeError("MAXIMUM_POSITION needs to be stated in the .env file \
                as a positive integer on the form: MAXIMUM_POSITION=50000")

        if not settings["USER_CONFIG"] and\
          not os.path.isfile(settings["USER_CONFIG"]):
            raise FileNotFoundError("No settings file found. Using default settings. \
                Missing file ", settings["USER_CONFIG"])

        if not settings["IP_ADDRESS"] and\
          not isinstance(settings["IP_ADDRESS"], str) and\
          not is_valid_ipv4_address(settings["IP_ADDRESS"]):
            raise TypeError("IP_ADDRESS needs to be stated in the .env file \
                as an IPv4 address on the form: IP_ADDRESS=192.168.0.150")

        if not settings["DEFAULT_REQUESTED_POSITION"] and\
          not isinstance(settings["DEFAULT_REQUESTED_POSITION"], int) and\
          not settings["DEFAULT_REQUESTED_POSITION"] > 0:
            raise TypeError("DEFAULT_REQUESTED_POSITION needs to be stated in the .env file \
                as a positive integer on the form: DEFAULT_REQUESTED_POSITION=50000")

        if not settings["SPEED"] and\
          not isinstance(settings["SPEED"], int) and\
          not settings["SPEED"] > 0:
            raise TypeError("SPEED needs to be stated in the .env file \
                as an integer on the form: SPEED=20000")

        if not settings["SPEED_OUT"] and\
          not isinstance(settings["SPEED_OUT"], int) and\
          not settings["SPEED_OUT"] > 0:
            raise TypeError("SPEED_OUT needs to be stated in the .env file \
                as an integer on the form: SPEED_OUT=20000")

        if not settings["SOFTWARE_VERSION"] and\
          not isinstance(settings["SOFTWARE_VERSION"], float) and\
          not settings["SOFTWARE_VERSION"] > 0:
            raise TypeError("SOFTWARE_VERSION needs to be stated in the .env file \
                as a float on the form: SOFTWARE_VERSION=1.0, where the first number \
                    increments major revisions and the second number minor revisions.")
    else:
        raise TypeError("Settings need to be on the form of a comma-separated dict/key-value pair. For example: {\"ip_address\": \"192.168.0.150\"}")

def export_check():
    pass
