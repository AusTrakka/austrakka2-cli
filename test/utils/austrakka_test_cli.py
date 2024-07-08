import os
from typing import List

from click.testing import CliRunner, Result

from austrakka.utils.context import CxtKey
from austrakka.utils.context import AusTrakkaCxt
from austrakka.utils.misc import AusTrakkaCliTopLevel
from test.utils.exceptions import CliTestException


PRODLIKE_DOMAIN = "austrakka.net"


class AusTrakkaTestCli:
    """
    A wrapper class around click.testing.CliRunner for invoking the AusTrakka
    CLI.
    """

    def __init__(self, austrakka_cli: AusTrakkaCliTopLevel):
        self._austrakka_cli = austrakka_cli
        self._runner = CliRunner()
        self._validate()

    def _validate(self) -> None:
        """
        Ensures that a valid test AusTrakka CLI can be created

        :raises CliTestException: there is a problem with the provided config
        """
        at_uri = os.getenv(AusTrakkaCxt.get_env_var_name(CxtKey.URI), '')
        if PRODLIKE_DOMAIN in at_uri:
            raise CliTestException(f"Unable to run tests against {at_uri}")

    def invoke(self, args: List[str]) -> Result:
        """
        Invoke the AusTrakka CLI

        :param args: verbatim subcommands, options and arguments for the CLI
        :return: result of invoking the command
        """
        return self._runner.invoke(self._austrakka_cli, args)
