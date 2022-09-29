import os
import typing as t
from gettext import gettext as _

from click.decorators import option
from click.core import Context
from click.core import Parameter
from click.decorators import FC
from rich.console import Console
from rich.markdown import Markdown

from austrakka import ROOT_DIR

README_PATH = os.path.join(ROOT_DIR, '..', 'README.md')

console = Console()


def man_option(
        *param_decls: str,
        **kwargs: t.Any,
) -> t.Callable[[FC], FC]:
    def callback(ctx: Context, _: Parameter, value: bool) -> None:
        if not value or ctx.resilient_parsing:
            return

        with open(README_PATH, "r+") as readme:
            console.print(Markdown(readme.read()))
        ctx.exit()

    if not param_decls:
        param_decls = ("--man",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", _("Show the man page and exit."))
    kwargs["callback"] = callback
    return option(*param_decls, **kwargs)