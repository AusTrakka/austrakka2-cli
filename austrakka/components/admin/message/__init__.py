from io import BufferedReader
import click

from austrakka.components.admin.message.feedback import feedback
from austrakka.components.admin.message.dl import dead_letter
from austrakka.components.admin.message.funcs import add_message
from austrakka.components.admin.message.funcs import metrics_message
from austrakka.components.admin.message.funcs import show_message
from austrakka.components.admin.message.funcs import list_message
from austrakka.components.admin.message.funcs import opt_queue_name
from austrakka.components.admin.message.funcs import opt_msg_id
from austrakka.utils.cmd_filter import show_admin_cmds
from austrakka.utils.output import table_format_option
from austrakka.utils.output import object_format_option


@click.group()
@click.pass_context
def message(ctx):
    """Commands related to messages"""
    ctx.context = ctx.parent.context


# pylint: disable=expression-not-assigned
message.add_command(dead_letter) if show_admin_cmds() else None
message.add_command(feedback) if show_admin_cmds() else None


@message.command('add')
@click.argument('file', type=click.File('r'))
@opt_queue_name()
def message_add(file: BufferedReader, queue: str):
    '''
    Add message to a queue. Accepts a json file.
    '''
    add_message(file, queue)


@message.command('metrics')
@opt_queue_name(required=False, default="")
@table_format_option()
def message_metrics(queue: str, out_format: str):
    '''
    List metrics for queues
    '''
    metrics_message(queue, out_format)


@message.command('show')
@opt_queue_name()
@opt_msg_id()
@object_format_option()
def message_show(queue: str, msg_id: int, out_format: str):
    '''
    Show contents of a message
    '''
    show_message(queue, msg_id, out_format)


@message.command('list')
@opt_queue_name()
@object_format_option()
def message_list(queue: str, out_format: str):
    '''
    List messages for a queue
    '''
    list_message(queue, out_format)
