import click

from austrakka.components.admin.message.dl.funcs import delete_dl, list_dl, resend_dl, show_dl, summary_dl
from austrakka.components.admin.message.funcs import opt_msg_id
from austrakka.components.admin.message.funcs import opt_queue_name
from austrakka.utils.output import FORMATS, table_format_option
from austrakka.utils.output import object_format_option

@click.group()
@click.pass_context
def dl(ctx):
    """Commands related to dead letter messages"""
    ctx.context = ctx.parent.context

@dl.command('show')
@opt_queue_name()
@opt_msg_id()
@object_format_option()
def dl_show(queue_name: str, msg_id: int, out_format: str):
    '''
    Show contents of dead letter message
    '''
    show_dl(queue_name, msg_id, out_format)


@dl.command('list')
@opt_queue_name(required=False, default="")
@object_format_option()
def dl_list(queue_name: str, out_format: str):
    '''
    List dead letter messages
    '''
    list_dl(queue_name, out_format)


@dl.command('delete')
@opt_queue_name()
@opt_msg_id()
def dl_delete(queue_name: str, msg_id: int):
    '''
    Delete a dead letter message
    '''
    delete_dl(queue_name, msg_id)


@dl.command('summary')
@table_format_option()
def dl_summary(out_format: str):
    '''
    Provides a count of all dead letter items for each queue
    '''
    summary_dl(out_format)


@dl.command('resend')
@opt_queue_name()
@opt_msg_id()
def dl_resend(queue_name: str, msg_id: int):
    '''
    Resend a dead letter message
    '''
    resend_dl(queue_name, msg_id)
