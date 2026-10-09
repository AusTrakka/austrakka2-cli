import click


def opt_process_auth_id(func):
    return click.option(
        '--id',
        'process_id',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_PROCESS_ID',
        help="Process account ID"
    )(func)


def opt_process_auth_secret(func):
    return click.option(
        '--secret',
        show_envvar=True,
        required=True,
        envvar='AT_AUTH_PROCESS_SECRET',
        help='Process account secret'
    )(func)
