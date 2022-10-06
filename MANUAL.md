# AusTrakka CLI
CLI for AusTrakka V2

## Environment Variables

- `AT_TOKEN`: AusTrakka auth token
- `AT_URI`: URI for API endpoint
- `AT_ENV`: Set to `dev` to log debugging
- `AT_LOG`: Set to `file` to redirecting logging to a temp file
- `AT_CMD_SET`: Set to `austrakka-admin` to display admin commands

All commands require `AT_URI` and `AT_TOKEN` to be set, except for `auth` commands.

## Authorisation

### User

Set the following env var
`export AT_TOKEN=$(austrakka auth user)`

### Process

Set the following env var
`export AT_TOKEN=$(austrakka auth process)`
