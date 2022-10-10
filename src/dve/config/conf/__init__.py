import os.path
import toml

from dve.config import data

_config = dict()

CONFIG_F_MAIN = "./config.toml"
CONFIG_S_MAIN = "main"
CONFIG_S_DEFAULT = CONFIG_S_MAIN


def config_name(what=CONFIG_S_DEFAULT):
    result = None
    if what == CONFIG_S_MAIN:
        result = CONFIG_F_MAIN
    if result is None:
        raise ValueError(f'Config Name unknown: "{what}", cannot load')
    return result

def config_path(what=CONFIG_S_DEFAULT):
    name = config_name(what)
    fn = os.path.join(data.DATA_WORK, name)
    result = os.path.normpath(fn)
    return result


def load_config(what=CONFIG_S_DEFAULT):
    fn = config_path(what)
    if not os.path.exists(fn):
        raise ValueError(f"Config Name {what} file not found: {fn}")
    raw_config = None
    try:
        with (open(fn)) as fd:
            raw_config = fd.read()
    except Exception as ex:
        print(type(ex))
        print(ex.args)
        print(ex)
        raise ex

    try:
        result = toml.loads(raw_config)
        return result
    except Exception as ex:
        print(type(ex))
        print(ex.args)
        print(ex)
        raise ex


def get_config(what=CONFIG_S_DEFAULT):
    global _config
    if not what in _config:
        handle = {
            "what": what,
            "loaded": True,
            "failed": False,
            "error": None,
            "data": None,
        }
        _config[what] = handle
        try:
            handle["data"] = load_config(what)

        except Exception as ex:
            handle["failed"] = True
            handle["error"] = ex
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex

    h = _config[what]
    result = h["data"]

    if result is None:
        ex = h["error"]
        raise ValueError(f"Config Name {what} not loaded: {type(ex)} {ex.args}")
    return result
