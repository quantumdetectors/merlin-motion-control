from .verify_ip import is_valid_ipv4_address
import os

def import_check(settings):
    if isinstance(settings,dict):
        key = "MAXIMUM_POSITION"
        if key in settings and\
          (not isinstance(settings["MAXIMUM_POSITION"], int) or\
          not settings["MAXIMUM_POSITION"] > 0):
            raise TypeError("MAXIMUM_POSITION needs to be stated in the .env file \
                as a positive integer on the form: MAXIMUM_POSITION=50000")

        key = "USER_CONFIG"
        if key in settings and\
          (not os.path.isfile(settings["USER_CONFIG"])):
            raise FileNotFoundError("No settings file found. Using default settings. \
                Missing file ", settings["USER_CONFIG"])

        key = "IP_ADDRESS"
        if key in settings and\
          (not isinstance(settings["IP_ADDRESS"], str) or\
          not is_valid_ipv4_address(settings["IP_ADDRESS"])):
            raise AttributeError("{} not a valid IPv4 address. IP_ADDRESS needs to be stated in the .env file \
                as an IPv4 address on the form: IP_ADDRESS=192.168.0.150".format(settings["IP_ADDRESS"]))

        key = "DEFAULT_REQUESTED_POSITION"
        if key in settings and\
          (not isinstance(settings["DEFAULT_REQUESTED_POSITION"], int) or\
          not settings["DEFAULT_REQUESTED_POSITION"] > 0):
            raise TypeError("DEFAULT_REQUESTED_POSITION needs to be stated in the .env file \
                as a positive integer on the form: DEFAULT_REQUESTED_POSITION=50000")

        key = "STANDBY_POSITION"
        if key in settings and\
          (not isinstance(settings["STANDBY_POSITION"], int) or\
          not settings["STANDBY_POSITION"] > 0):
            raise TypeError("STANDBY_POSITION needs to be stated in the .env file \
                as a positive integer on the form: STANDBY_POSITION=120000")

        key = "SPEED"
        if key in settings and\
          (not isinstance(settings["SPEED"], int) or\
          not settings["SPEED"] > 0):
            raise TypeError("SPEED needs to be stated in the .env file \
                as an integer on the form: SPEED=20000")

        key = "SPEED_OUT"
        if key in settings and\
          (not isinstance(settings["SPEED_OUT"], int) or\
          not settings["SPEED_OUT"] > 0):
            raise TypeError("SPEED_OUT needs to be stated in the .env file \
                as an integer on the form: SPEED_OUT=20000")

        key = "SOFTWARE_VERSION"
        if key in settings and\
          (not isinstance(settings["SOFTWARE_VERSION"], str) or\
          not float(settings["SOFTWARE_VERSION"]) > 0):
            raise TypeError("SOFTWARE_VERSION needs to be stated in the .env file \
                as a float on the form: SOFTWARE_VERSION=1.0, where the first number \
                    increments major revisions and the second number minor revisions.")
    else:
        raise TypeError("Settings need to be on the form of a comma-separated dict/key-value pair. For example: {\"ip_address\": \"192.168.0.150\"}")

def export_check():
    pass
