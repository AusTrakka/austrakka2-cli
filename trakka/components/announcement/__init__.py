import click

from trakka.components.announcement.funcs import create_announcement
from trakka.utils.cmd_filter import hide_admin_cmds
from trakka.utils.options import opt_user_identifier, opt_announcement_subject, opt_announcement_body


@click.group()
@click.pass_context
def announcement(ctx):
    """Commands related to announcements"""
    ctx.context = ctx.parent.context

@announcement.command(
    'create',
    hidden=hide_admin_cmds(),
    help='Create an announcement'
)
@opt_user_identifier(required=True, multiple=True)
@opt_announcement_subject()
@opt_announcement_body()
def announcement_create(subject: str, body: str, user_id: list[str]):
    create_announcement(subject, body, user_id)