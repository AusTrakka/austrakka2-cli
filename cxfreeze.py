from cx_Freeze import setup
from austrakka import __version__ as VERSION

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
    ],
}

setup(
    name="trakka",
    version=VERSION,
    description="Trakka CLI",
    options={"build_exe": build_exe_options},
    executables=[{"script": "austrakka/main.py", "base": "console", "target_name": "trakka"}],
)
