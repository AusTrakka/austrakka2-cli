from loguru import logger
from trakka.utils.context import CxtKey, TrakkaCxt

AUSTRAKKA_ADMIN = 'austrakka-admin'
TRAKKA_ADMIN = 'admin'
USER = 'user'

_deprecation_warning_printed = False

def show_admin_cmds():
    cmd_set = TrakkaCxt.get_env_var_value(CxtKey.CMD_SET, '')
    deprecation_warning(cmd_set)
    return cmd_set and cmd_set.lower() in [AUSTRAKKA_ADMIN, TRAKKA_ADMIN]


def hide_admin_cmds():
    return not show_admin_cmds()


def deprecation_warning(value: str):
    # This global flag is required as this function will be called
    # for every instance of a admin command
    global _deprecation_warning_printed
    if _deprecation_warning_printed:
        return
    if value == AUSTRAKKA_ADMIN:
        env_var_names = ", ".join(TrakkaCxt.get_env_var_names(CxtKey.CMD_SET))
        # This unfortunately occurs before we've set up our logger
        # as it's part of the click initialisation, which
        # means this line might look different; it's temporary,
        # and as only internal users are using this flag we can
        # remove it sooner.
        logger.warning("Value " + AUSTRAKKA_ADMIN + " for env vars " + env_var_names + " is deprecated and will be replaced with " + TRAKKA_ADMIN + " in a future release.")
        _deprecation_warning_printed = True
