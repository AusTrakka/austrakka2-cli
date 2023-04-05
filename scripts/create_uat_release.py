import json
import os
import types

import httpx

AT_CLI_PACKAGE_GUID = os.environ.get("AT_CLI_PACKAGE_GUID")
DEVOPS_TOKEN = os.environ.get("DEVOPS_TOKEN")

SETUP_ENTRY_POINT = 'austrakka=austrakka.main:main'
UAT_SETUP_ENTRY_POINT = 'austrakka-uat=austrakka.main:main'

SETUP_PACKAGE_NAME = 'name="austrakka"'
UAT_SETUP_PACKAGE_NAME = 'name="austrakka-uat"'

dir_path = os.path.dirname(os.path.realpath(__file__))

version_module = types.ModuleType('version')

VERSION_FILE_PATH = os.path.join(dir_path, "..", "austrakka", "__init__.py")
SETUP_FILE_PATH = os.path.join(dir_path, "..", "setup.py")

with open(VERSION_FILE_PATH, "r") as version_file_data:
    exec(version_file_data.read(), version_module.__dict__)

VERSION = version_module.__version__

resp = httpx.get(
    f'https://feeds.dev.azure.com/mduphl/austrakka/_apis/packaging/'
    + f'feeds/austrakka-feed/packages/{AT_CLI_PACKAGE_GUID}/versions',
    headers={
        'Content-Type': 'application/json-patch+json'
    },
    auth=('', DEVOPS_TOKEN)
)

json_obj = json.loads(resp.text)

# get list of all versions
versions = [
    package_version['protocolMetadata']['data']['version']
    for package_version
    in json_obj['value']
]

# filter out non-related versions
versions = [version for version in versions if version.startswith(VERSION)]

version_list = VERSION.split('.')

version_list.append(str(len(versions) + 1))

next_version_text = '.'.join(version_list)

print(f"Creating UAT release {next_version_text}")

with open(VERSION_FILE_PATH, 'r+') as version_file:
    version_file_data = version_file.read()
    version_file_data = version_file_data.replace(VERSION, next_version_text)
    version_file.seek(0)
    version_file.truncate()
    version_file.write(version_file_data)

with open(SETUP_FILE_PATH, 'r+') as setup_file:
    setup_file_data = setup_file.read()
    setup_file_data = setup_file_data.replace(
        SETUP_ENTRY_POINT,
        UAT_SETUP_ENTRY_POINT
    )
    setup_file_data = setup_file_data.replace(
        SETUP_PACKAGE_NAME,
        UAT_SETUP_PACKAGE_NAME
    )
    setup_file.seek(0)
    setup_file.truncate()
    setup_file.write(setup_file_data)
