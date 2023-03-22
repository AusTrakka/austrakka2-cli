# AusTrakka CLI

Command line interface for AusTrakka V2.

## Installation

Install with 
```
python -m pip install austrakka
```

You will need to set the environment variable `AT_URI` to the value provided by the AusTrakka team.
You may wish to add this to your `.bashrc` or `.zshrc` file.

To use the CLI, you must log in by setting the `AT_TOKEN` environment variable using the 
`austrakka user auth` command (see User Authorisation, below). You may wish to configure 
a login command for convenience:
```
alias at-login="export AT_TOKEN=\$(austrakka auth user)"
```
You may wish to add this to your `.bashrc` or `.zshrc` file.

### Install into a conda environment (optional)

If you wish to create a conda environment named `austrakka` with the necessary environment 
variables set and the `at-login` alias, run:
```
conda create -n austrakka python=3.9
conda activate austrakka
python -m pip install austrakka
conda env config vars set AT_URI="[value provided by AusTrakka team]"
mkdir -p ${CONDA_PREFIX}/etc/conda/activate.d
echo "alias at-login=\"export AT_TOKEN=\\\$(austrakka auth user)\"" > ${CONDA_PREFIX}/etc/conda/activate.d/austrakka-alias.sh
```

You can then use
```
conda activate austrakka
at-login
```
in order to use the CLI.

### Updating the CLI

To update to the latest version, run 
```
python -m pip install --upgrade austrakka
```
If you have installed the CLI into a conda environment, you should first activate it with `conda activate austrakka`.

## Running the CLI

Before you can use the CLI, you must log in as described below, to allow the CLI to use your AusTrakka credentials. 
Your authorisation will expire after a period and you will need to log in again.

### User Authorisation

Most users will want to use the CLI this way.

Set the following environment variable:
```
export AT_TOKEN=$(austrakka auth user)
```

If you have configured a login command as described above, you can instead run 
```
at-login
```

Either way, you should be directed to log in via a browser and enter a code to authorise the CLI.

### Process Authorisation

This authorisation mode is intended for long-term automated processes. Most users will not need it. 

To authorise a process, you'll need to set the following environment variables:
```bash
AT_AUTH_PROCESS_ID
AT_AUTH_PROCESS_SECRET
```
Values for `AT_AUTH_PROCESS_ID` and `AT_AUTH_PROCESS_SECRET` will be provided to you by the AusTrakka team. Note that the secret value is sensitive.

Once these variables are set, run the following to authorise:
```
export AT_TOKEN=$(austrakka auth process)
```

### Using the CLI

The CLI has a subcommand structure. Run 
```
austrakka -h
```
to see available subcommands.

Run e.g. 
```
austrakka metadata -h
```
to see available commands to manipulate metadata.

Run e.g. 
```
austrakka metadata add -h
```
to see the usage of the `metadata add` command to upload metadata files.

## Environment Variables Reference

| Name             | Description                                                                                                                                     |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `AT_TOKEN`       | AusTrakka auth token                                                                                                                            |
| `AT_URI`         | URI for API endpoint                                                                                                                            |
| `AT_ENV`         | Set to `dev` to log debugging                                                                                                                   |
| `AT_LOG`         | Set to `file` to redirecting logging to a temp file                                                                                             |
| `AT_CMD_SET`     | Set to `austrakka-admin` to display admin commands (these will not actually run successfully unless you have an appropriate role on the server) |
| `AT_VERIFY_CERT` | Verifies the cert used by the AusTrakka backend                                                                                                 |

All commands require `AT_URI` and `AT_TOKEN` to be set, except for `auth` commands.

## Project Structure

Each logical component of the system has its own package under `austrakka/`. Eg. `austrakka/job`.
Components that are children of another component are nested beneath. Eg. `austrakka/job/instance`.

Each component package contains the following files:

| File          | Purpose                                                                                                                                                                                                                                      |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `__init__.py` | Contains the Click commands offered by the component. Note that even if a component does not have any commands associated with it, this file must exist for the final build to include it.                                                   |
| `funcs.py`    | Any functions associated with the component.                                                                                                                                                                                                 |
| `opts.py`     | Click command line options associated with the component. Defined here so they can be reused across the CLI. Eg. `--species` is used for multiple commands. The species CLI option is defined here and imported to all commands that use it. |
| `enums.py`    | Any enumerations associated with the component.                                                                                                                                                                                              |
