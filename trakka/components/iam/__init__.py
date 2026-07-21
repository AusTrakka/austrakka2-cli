# pylint: disable=expression-not-assigned
import click

from trakka.utils.privilege import TENANT_RESOURCE
from .privilege import privilege_subcommands
from .scope import scope
from .role import role


@click.group()
@click.pass_context
def iam(ctx):
    """Commands related to role based access control"""
    ctx.context = ctx.parent.context


iam.add_command(scope)
iam.add_command(role)
iam.add_command(privilege_subcommands(TENANT_RESOURCE))
