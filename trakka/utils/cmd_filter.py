import os

AUSTRAKKA_ADMIN = 'austrakka-admin'
TRAKKA_ADMIN = 'trakka-admin'


def show_admin_cmds():
    cmd_set = os.getenv('AT_CMD_SET')
    return cmd_set and cmd_set.lower() in [AUSTRAKKA_ADMIN, TRAKKA_ADMIN]


def hide_admin_cmds():
    return not show_admin_cmds()
