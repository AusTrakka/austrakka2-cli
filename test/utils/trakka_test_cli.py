import os
from typing import List

from click.testing import CliRunner, Result

from trakka.utils.context import CxtKey
from trakka.utils.context import TrakkaCxt
from trakka.utils.misc import TrakkaCliTopLevel
from test.utils.exceptions import CliTestException


PRODLIKE_DOMAIN = "austrakka.net"


class TrakkaTestCli:
    """
    A wrapper class around click.testing.CliRunner for invoking the Trakka
    CLI.
    """

    def __init__(self, trakka_cli: TrakkaCliTopLevel):
        self._trakka_cli = trakka_cli
        self._runner = CliRunner()
        self._validate()

    def _validate(self) -> None:
        """
        Ensures that a valid test Trakka CLI can be created

        :raises CliTestException: there is a problem with the provided config
        """
        at_uri = os.getenv(TrakkaCxt.get_env_var_name(CxtKey.URI), '')
        if PRODLIKE_DOMAIN in at_uri:
            raise CliTestException(f"Unable to run tests against {at_uri}")

    def invoke(self, args: List[str]) -> Result:
        """
        Invoke the Trakka CLI

        :param args: verbatim subcommands, options and arguments for the CLI
        :return: result of invoking the command
        """
        print("Invoking CLI", args)
        return self._runner.invoke(self._trakka_cli, args)
