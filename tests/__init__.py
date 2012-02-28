from ConfigParser import ConfigParser

def get_config():
    config = ConfigParser({}, dict)
    config.read("tests/tests.ini") 

    c = config._sections["sanction"]
    del c["__name__"]

    if "http_debug" in c:
        c["http_debug"] = c["http_debug"] == "true"

    return config._sections["sanction"]

