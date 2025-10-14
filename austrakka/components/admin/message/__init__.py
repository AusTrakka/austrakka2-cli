from io import BufferedReader
import click

from austrakka.components.admin.message.dl import dead_letter
from austrakka.components.admin.message.funcs import add_message
from austrakka.components.admin.message.funcs import opt_queue_name
from austrakka.utils.cmd_filter import show_admin_cmds


@click.group()
@click.pass_context
def message(ctx):
    """Commands related to messages"""
    ctx.context = ctx.parent.context


# pylint: disable=expression-not-assigned
message.add_command(dead_letter) if show_admin_cmds() else None


@message.command('add')
@click.argument('file', type=click.File('r'))
@opt_queue_name()
def message_add(file: BufferedReader, queue_name: str):
    '''
    Add message to a queue. Accepts a json file.
    '''
    add_message(file, queue_name)
