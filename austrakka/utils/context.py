from enum import Enum

from click import get_current_context

from austrakka.utils.exceptions import AusTrakkaCliException


CLI_PREFIX = 'AT'


class CxtKey(Enum):
    """
    Enums for our top-level options and environment variables
    """
    URI = 'uri'
    TOKEN = 'token'
    SKIP_CERT_VERIFY = 'skip_cert_verify'
    USE_HTTP2 = 'use_http2'
    SKIP_VERSION_CHECK = 'skip_version_check'
    LOG_LEVEL = 'log_level'


class AusTrakkaCxt:
    """
    Provides helper methods to deal with top-level options and environment variables
    """
    @staticmethod
    def get_value(ctx_key: CxtKey):
        """
        This method relies on a click context being active.
        If there is no click context, eg. top level exception catch, then 
        directly probe the environment
        :param ctx_key: context key
        :return: value of the context key
        """
        try:
            return get_current_context().parent.context[ctx_key.value]
        except RuntimeError as ex:
            raise AusTrakkaCliException(
                f"Error accessing CLI context for key {ctx_key.name}."
                + "Context may not be active, or key does not exist." 
            ) from ex 

    @staticmethod
    def get_option_name(ctx_key: CxtKey):
        """
        :param ctx_key: context key
        :return: A cli option name string. eg. --option-name
        """
        return f"--{ctx_key.value.replace('_', '-')}"

    @staticmethod
    def get_env_var_name(ctx_key: CxtKey):
        """
        :param ctx_key: context key
        :return: The env var name for the context key
        """
        return f"{CLI_PREFIX}_{ctx_key.value.upper()}"
