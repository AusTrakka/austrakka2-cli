import os

from cx_Freeze import setup
from trakka import __version__ as VERSION

build_dir = os.environ.get("TRAKKA_CLI_BUILD_DIR")

build_exe_options = {
    "excludes": [],
    "zip_include_packages": [
        "azure-identity",
        "click",
        "loguru",
        "pandas",
        "tabulate",
        "cryptography",
        "semver",
        "httpx[http2]",
        "biopython",
        "XlsxWriter",
        "dateparser",
        "dateparser.data",
        "dateparser.data.date_translation_data",
        "dateparser.data.date_translation_data.en",
    ],
    "includes": [
        "dateparser.languages.loader",
        "dateparser.conf",
        "dateparser.date",
    ],
    "packages": [
        "dateparser",
        "dateparser.data",
        "dateparser.data.date_translation_data",
        "dateparser.data.date_translation_data.en",
    ],
}
if build_dir is not None:
    print("Building trakka in " + build_dir)
    build_exe_options["build_exe"] = build_dir

setup(
    name="trakka",
    version=VERSION,
    description="Trakka CLI",
    options={"build_exe": build_exe_options},
    executables=[{"script": "trakka/main.py", "base": "console", "target_name": "trakka"}],
)
