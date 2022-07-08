# AusTrakka CLI
CLI for AusTrakka V2

## Environment Variables

| Name         | Description                                         |
|--------------|-----------------------------------------------------|
| `AT_TOKEN`   | AusTrakka auth token                                |
| `AT_URI`     | URI for API endpoint                                |
| `AT_ENV`     | Set to `dev` to log debugging                       |
| `AT_LOG`     | Set to `file` to redirecting logging to a temp file |
| `AT_CMD_SET` | Set to `austrakka-admin` to display admin commands  |

All commands require `AT_URI` and `AT_TOKEN` to be set, except for `auth` commands.

## Authorisation

### User

Set the following env var
`export AT_TOKEN=$(austrakka auth user)`

### Process

Set the following env var
`export AT_TOKEN=$(austrakka auth process)`

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
