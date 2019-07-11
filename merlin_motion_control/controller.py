import config

class app():
    def run():

        try:
            settings = config.load_user_settings()
            for k,v in settings.items():
                print(k,v)
        except AttributeError as e:
            print(e.__class__, "".join(e.args))
        except FileNotFoundError as e:
            print(e.__class__, "".join(e.args))
            settings = {
                "ip_address":config.default_ip(),
                "default_requested_position":config.default_requested_position(),
                "speed":config.default_speed(),
                "speed_out":config.default_speed_out()
            }
            print("Default settings are:")
            for k,v in settings.items():
                print(k,v)
