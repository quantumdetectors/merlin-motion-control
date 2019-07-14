from models.verify_ip import is_valid_ipv4_address


def import_check(settings):
    if isinstance(settings,dict):

        key = "ip_address"
        if key in settings and\
          (not isinstance(settings["ip_address"], str) or\
          not is_valid_ipv4_address(settings["ip_address"])):
            raise AttributeError("{} not a valid IPv4 address or has not been stated correctly in the settings file. \
                Using default value.".format(settings["ip_address"]))


        key = "default_requested_position"
        if key in settings and\
          (not isinstance(settings["default_requested_position"], int) or\
          not settings["default_requested_position"] > 0):
            raise ValueError("default_requested_position has not been stated correctly in the settings file. \
                Using default value.")

        key = "speed"
        if key in settings and\
          (not isinstance(settings["speed"], int) or\
          not settings["speed"] > 0):
            raise TypeError("speed has not been stated correctly in the settings file. \
                Using default value.")

        key = "speed_out"
        if key in settings and\
          (not isinstance(settings["speed_out"], int) or\
          not settings["speed_out"] > 0):
            raise BlockingIOError("speed_out has not been stated correctly in the settings file. \
                Using default value.")

    else:
        raise SyntaxError("Settings need to be on the form of a comma-separated dict/key-value pair. For example: {\"ip_address\": \"192.168.0.150\"}")

def export_check():
    pass
