from austrakka.utils.output import RESPONSE_MESSAGE
from austrakka.utils.output import RESPONSE_MESSAGES
from austrakka.utils.output import RESPONSE_TYPE
from austrakka.utils.output import RESPONSE_TYPE_ERROR
from austrakka.utils.output import RESPONSE_TYPE_WARNING
from austrakka.utils.output import RESPONSE_TYPE_SUCCESS


class UnknownResponseException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class FailedResponseException(Exception):
    def __init__(self, parsed_resp, status_code=None):
        self.parsed_resp = parsed_resp
        self.message = f'Request failed: {parsed_resp}'
        self.status_code = status_code
        super().__init__(self.message)

    def get_messages(self, message_type: str):
        return [
            message[RESPONSE_MESSAGE]
            for message
            in self.parsed_resp[RESPONSE_MESSAGES]
            if message[RESPONSE_TYPE] == message_type
        ]

    def get_error_messages(self):
        return self.get_messages(RESPONSE_TYPE_ERROR)

    def get_warning_messages(self):
        return self.get_messages(RESPONSE_TYPE_WARNING)

    def get_success_messages(self):
        return self.get_messages(RESPONSE_TYPE_SUCCESS)


class IncorrectHashException(Exception):
    pass
