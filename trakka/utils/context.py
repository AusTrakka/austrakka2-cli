from enum import Enum
import os
from typing import List

from click import get_current_context
from loguru import logger

from trakka.utils.exceptions import TrakkaCliException


AT_CLI_PREFIX = 'AT'
TRAKKA_CLI_PREFIX = 'TRAKKA'


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
    SESSION_ID = 'session_id'
    TIMEZONE = 'timezone'
    CMD_SET = 'cmd_set'
    AUTH_PROCESS_SECRET = 'auth_process_secret'
    AUTH_PROCESS_ID = 'auth_process_id'
    AUTH_APP_URI = 'auth_app_uri'
    AUTH_CLIENT_ID = 'auth_client_id'
    AUTH_TENANT_ID = 'auth_tenant_id'


class TrakkaCxt:
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
            raise TrakkaCliException(
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
    def _get_at_env_var_name(ctx_key: CxtKey):
        """
        :param ctx_key: context key
        :return: The env var name for the context key
        """
        return f"{AT_CLI_PREFIX}_{ctx_key.value.upper()}"

    @staticmethod
    def _get_trakka_env_var_name(ctx_key: CxtKey):
        """
        :param ctx_key: context key
        :return: The env var name for the context key
        """
        return f"{TRAKKA_CLI_PREFIX}_{ctx_key.value.upper()}"

    @staticmethod
    def get_env_var_names(ctx_key: CxtKey) -> List[str]:
        """
        :param ctx_key: context key
        :return: The env var name for the context key
        """
        return [
            TrakkaCxt._get_trakka_env_var_name(ctx_key),
            TrakkaCxt._get_at_env_var_name(ctx_key),
        ]

    @staticmethod
    def get_env_var_value(ctx_key: CxtKey, default) -> str:
        """
        Use in situations where we don't have access to the click context.
        :param ctx_key: context key
        :return: The env var value
        """
        trakka_name = TrakkaCxt._get_trakka_env_var_name(ctx_key)
        at_name = TrakkaCxt._get_at_env_var_name(ctx_key)
        if trakka_name in os.environ:
            return os.getenv(trakka_name, default)
        if at_name in os.environ:
            return os.getenv(at_name, default)
        return default

    @staticmethod
    def check_deprecated_env_vars():
        for k in CxtKey:
            trakka_name = TrakkaCxt._get_trakka_env_var_name(k)
            at_name = TrakkaCxt._get_at_env_var_name(k)
            if at_name in os.environ and trakka_name not in os.environ:
                logger.warning("Environment variable " + at_name 
                    + " is deprecated and will be replaced with " 
                    + trakka_name + " in a future release.")
