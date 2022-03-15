class UnknownResponseException(Exception):
    pass


class FailedResponseException(Exception):
    def __init__(self, parsed_resp):
        self.parsed_resp = parsed_resp
        self.message = f'Request failed: {parsed_resp}'
        super().__init__(self.message)
