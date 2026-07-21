# Trakka CLI

Command line interface for Trakka APIs.

## Getting started with the CLI

The Trakka CLI is a command-line interface for interacting with the Trakka platform.
To use it, you will need a Trakka account which grants the relevant roles and permissions in any organisation or 
project you wish to interact with.

The CLI can be used for several purposes, including:

- Submitting sequence data
- Submitting metadata (sample, sequence and epidemiological metadata)
- Retrieving data for analysis
- Uploading analysis results (trees and analysis-derived metadata)

Note that currently, sequence data can only be submitted using the CLI, and cannot be submitted via the web interface.

## Installation

### Standalone CLI

Currently only supported on Linux:

`curl -o- https://raw.githubusercontent.com/AusTrakka/austrakka2-cli/refs/heads/master/scripts/install | bash`

This will install `trakka` to `~/.local/bin`. You can pass a custom directory like this:

`curl -o- https://raw.githubusercontent.com/AusTrakka/austrakka2-cli/refs/heads/master/scripts/install | bash -s [OTHER_DIR]`

### Using Python

The CLI requires Python to run. If you would like to use conda to install Python, install the CLI, and save the necessary environment variables,
you can first install either Miniforge (https://github.com/conda-forge/miniforge) or Miniconda (https://docs.conda.io/en/latest/miniconda.html). We recommend Miniforge for most users.

Note that as a part of installing the CLI, you will need to set the environment's `TRAKKA_URI` variable.

### Install into a conda environment (optional but recommended)

If you wish to create a conda environment named `trakka` with the necessary environment 
variables set and the `at-login` alias, run:
```
conda create -n trakka python=3.12
conda activate trakka
python -m pip install trakka
conda env config vars set TRAKKA_URI=[VALUE]
mkdir -p ${CONDA_PREFIX}/etc/conda/activate.d
echo "alias at-login=\"export TRAKKA_TOKEN=\\\$(trakka auth user)\"" > ${CONDA_PREFIX}/etc/conda/activate.d/trakka-alias.sh
```
Note that the last two lines are valid only for Linux/Mac and will not work on Windows. These lines create an alias `at-login` 
in the conda environment, which will log you in to the CLI.

You can then use
```
conda activate trakka
at-login
```
in order to use the CLI. See _User Authentication_ below for alternative login methods.

### Install without conda

If you are using Windows, and are not a WSL or Powershell user, it is strongly recommended to use conda (see above).

To install without conda, simply install with 
```
python -m pip install trakka
```

You will need to set the environment variable `TRAKKA_URI`.
You can do this by running:

> #### Mac / Linux
>```
>export TRAKKA_URI=[VALUE]
>```
>You may wish to add this to your `.bashrc` or `.zshrc` file.

>#### Windows: Powershell
>```
>$Env:TRAKKA_URI = [VALUE]
>```

To use the CLI, you must log in by setting the `TRAKKA_TOKEN` environment variable using the 
`trakka auth user` command (see User Authentication, below). 

> #### Mac / Linux
>You may wish to configure 
>a login command for convenience:
>```
>alias at-login="export TRAKKA_TOKEN=\$(trakka auth user)"
>```
>You may wish to add this to your `.bashrc` or `.zshrc` file.

> #### Windows: Powershell
>You may wish to configure 
>a login command for convenience:
>```
>Function at-login { $Env:TRAKKA_TOKEN = trakka auth user }
>```
>You may wish to add this to your `config.ps1` file.

### Updating the CLI

To update to the latest version, run 
```
python -m pip install --upgrade trakka
```
If you have installed the CLI into a conda environment, you should first activate it with `conda activate trakka`:
```
conda activate trakka
python -m pip install --upgrade trakka
```

## Logging in

Before you can use the CLI, you must log in as described below, to allow the CLI to use your Trakka credentials. 
Your authorisation will expire after a period and you will need to log in again.

### User Authentication

Most users will want to log in to the CLI this way.

For any of these methods, you should be directed to log in via a browser and enter a code to authorise the CLI. 
This browser-based login uses your institutional credentials, i.e. the same credentials you use to log in 
to the Trakka web interface, and will authenticate you via your institution's identity provider.

>#### Mac / Linux
>If you have configured a login command as described above, you can simply run
>```
>at-login
>``` 
>
>Otherwise, you will need to set the `TRAKKA_TOKEN` environment variable. In a Mac or Linux environment you can run:
>```
>export TRAKKA_TOKEN=$(trakka auth user)
>```

>#### Windows: Powershell
>
>```
>$Env:TRAKKA_TOKEN = trakka auth user
>```

>#### Windows: Cmd
>
>Set the `TRAKKA_TOKEN` environment variable by first running
>```
>trakka auth user
>```
>to obtain a token string, and then running 
>```
>set TRAKKA_TOKEN=<output of previous command>
>```
>:w
> to set the environment variable.

### Process Authentication

This authentication mode is intended for long-term automated processes. Most users will not need it. 

To authenticate a process, you'll need to set the following environment variables:
```bash
TRAKKA_AUTH_PROCESS_ID
TRAKKA_AUTH_PROCESS_SECRET
```
Values for `TRAKKA_AUTH_PROCESS_ID` and `TRAKKA_AUTH_PROCESS_SECRET` will be provided to you by the Trakka team. Note that the secret value is sensitive.

Once these variables are set, run the following to authorise:

>#### Mac/Linux
>```
>export TRAKKA_TOKEN=$(trakka auth process)
>```

>#### Windows: Powershell
>```
>$Env:TRAKKA_TOKEN = trakka auth process
>```

>#### Windows: Cmd
>Set the `TRAKKA_TOKEN` environment variable by first running
>```
>trakka auth process
>```
>to obtain a token string, and then running 
>```
>set TRAKKA_TOKEN=<output of previous command>
>```
>to set the environment variable.


## Using the CLI

The CLI has a subcommand structure. Run 
```
trakka -h
```
to see available subcommands.

Run e.g. 
```
trakka metadata -h
```
to see available commands to manipulate metadata.

Run e.g. 
```
trakka metadata add -h
```
to see the usage of the `metadata add` command to upload metadata files.

## Environment Variables Reference

| Name                    | Description                                                                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `TRAKKA_TOKEN`              | Trakka auth token                                                                                                                            |
| `TRAKKA_URI`                | URI for API endpoint                                                                                                                            |
| `TRAKKA_LOG_LEVEL`          | Level of logging                                                                                                                                |
| `TRAKKA_LOG`                | Set to `file` to redirecting logging to a temp file                                                                                             |
| `TRAKKA_CMD_SET`            | Set to `trakka-admin` to display admin commands (these will not actually run successfully unless you have an appropriate role on the server) |
| `TRAKKA_TIMEZONE`           | Set to change the default timezone used for datetime display and parsing. Default if unset is to use your local timezone.                       |
| `TRAKKA_SKIP_CERT_VERIFY`   | Skips verification of the cert used by the Trakka backend                                                                                    |
| `TRAKKA_SKIP_VERSION_CHECK` | Skips checking of new CLI version                                                                                                               |
| `TRAKKA_USE_HTTP2`          | Uses HTTP2 (experimental)                                                                                                                       |

All commands require `TRAKKA_URI` and `TRAKKA_TOKEN` to be set, except for `auth` commands.

## Project Structure

Each logical component of the system has its own package under `trakka/`. Eg. `trakka/job`.
Components that are children of another component are nested beneath. Eg. `trakka/job/instance`.

Each component package contains the following files:

| File          | Purpose                                                                                                                                                                                                                                      |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `__init__.py` | Contains the Click commands offered by the component. Note that even if a component does not have any commands associated with it, this file must exist for the final build to include it.                                                   |
| `funcs.py`    | Any functions associated with the component.                                                                                                                                                                                                 |
| `opts.py`     | Click command line options associated with the component. Defined here so they can be reused across the CLI. Eg. `--species` is used for multiple commands. The species CLI option is defined here and imported to all commands that use it. |
| `enums.py`    | Any enumerations associated with the component.                                                                                                                                                                                              |


## Build

```bash
pipenv install --python=3.14 --dev
pipenv run ./scripts/build [OUTPUT_DIR]
```
