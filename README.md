# austrakka2-cli
CLI for AusTraka V2

## Environment Variables

| Name       | Description                                         |
| ---------- | --------------------------------------------------- |
| `AT_TOKEN` | AusTrakka auth token                                |
| `AT_URI`   | URI for API endpoint                                |
| `AT_ENV`   | Set to `dev` to log debugging                       |
| `AT_LOG`   | Set to `file` to redirecting logging to a temp file |

All commands require `AT_URI` and `AT_TOKEN` to be set, except for `auth` commands.


## Authorisation

### User

Set the following env var
`export AT_TOKEN=$(austrakka auth user)`

### Process

Set the following env var
`export AT_TOKEN=$(austrakka auth process)`
