import os

AUSTRAKKA_ADMIN = 'austrakka-admin'


def show_admin_cmds():
    cmd_set = os.getenv('AT_CMD_SET')
    return cmd_set and cmd_set.lower() == AUSTRAKKA_ADMIN


def hide_admin_cmds():
    return not show_admin_cmds()
