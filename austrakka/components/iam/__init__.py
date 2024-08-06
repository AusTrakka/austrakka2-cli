from austrakka.utils.options import *
from .privilege import privilege
from .scope import scope
from .role import role
from .tenant import tenant


@click.group()
@click.pass_context
def iam(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


iam.add_command(scope)
iam.add_command(role)
iam.add_command(privilege)
iam.add_command(tenant)
