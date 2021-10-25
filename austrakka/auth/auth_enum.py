from enum import Enum


class Auth(Enum):
    AUTH_URL = 'https://login.microsoftonline.com'
    TENANT_ID = '0e5bf3cf-1ff4-46b7-9176-52c538c22a4d'
    CLIENT_ID = '16292c74-3a1d-4664-9f65-edb167bf199b'
    REDIRECT_URI = 'http://localhost:8080'
    APP_ID = 'api://df125604-3b75-46d3-a8ea-e54dc3b5e402/AAP-AusTrakka-API'
    KEY_VAULT_URI = 'https://kvautrdevase01.vault.azure.net'
    SUBSCRIPTION_KEY = 'd03bb1ce7427476e83178fc949c33e06'
