import click

from austrakka.components.admin.message.feedback.funcs import delete_feedback
from austrakka.components.admin.message.feedback.funcs import list_feedback
from austrakka.components.admin.message.feedback.funcs import show_feedback
from austrakka.components.admin.message.funcs import opt_msg_id
from austrakka.components.admin.message.funcs import opt_queue_name
from austrakka.utils.output import object_format_option

@click.group('feedback')
@click.pass_context
def feedback(ctx):
    """Commands related to feedback messages"""
    ctx.context = ctx.parent.context

@feedback.command('show')
@opt_msg_id()
@object_format_option()
def feedback_show(msg_id: int, out_format: str):
    '''
    Show contents of feedback message
    '''
    show_feedback(msg_id, out_format)


@feedback.command('list')
@object_format_option()
def feedback_list(out_format: str):
    '''
    List feedback messages
    '''
    list_feedback(out_format)


@feedback.command('delete')
@opt_msg_id()
def feedback_delete(msg_id: int):
    '''
    Delete a feedback message
    '''
    delete_feedback(msg_id)
