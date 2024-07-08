import os
from typing import List

from click.testing import CliRunner, Result

from austrakka.utils.context import CxtKey
from austrakka.utils.context import AusTrakkaCxt 
from austrakka.utils.misc import AusTrakkaCliTopLevel
from test.utils.exceptions import CliTestException


PRODLIKE_DOMAIN = "austrakka.net"

class AusTrakkaTestCli:
    def __init__(self, austrakka_cli: AusTrakkaCliTopLevel):
        self._austrakka_cli = austrakka_cli
        self._runner = CliRunner()
        self._validate()
        
    def _validate(self) -> None:
        at_uri = os.getenv(AusTrakkaCxt.get_env_var_name(CxtKey.URI), '')
        if PRODLIKE_DOMAIN in at_uri: 
            raise CliTestException(f"Unable to run tests against {at_uri}") 


    def invoke(self, args: List[str]) -> Result:
        return self._runner.invoke(self._austrakka_cli, args)

