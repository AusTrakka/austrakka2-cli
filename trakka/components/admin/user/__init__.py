import click

from trakka.components.admin.user.funcs import update_object_id
from trakka.utils.options import opt_identifier, opt_user_object_id

@click.group('user')
@click.pass_context
def user(ctx):
    """Commands related to users"""
    ctx.context = ctx.parent.context

@user.command('update-object-id')
@opt_identifier(help="User Identifier")
@opt_user_object_id()
def object_id_update(identifier: str, user_id: str):
    '''
    Update a user's Azure object ID
    '''
    update_object_id(identifier, user_id)
