### AusTrakka CLI contributing guide

## Project Structure

Each logical component of the system has its own package under `austrakka/`. Eg. `austrakka/job`.
Components that are children of another component are nested beneath. Eg. `austrakka/job/instance`.

Each component package contains the following files:

- `__init__.py`: Contains the Click commands offered by the component. Note that even if a component does not have any commands associated with it, this file must exist for the final build to include it.
- `funcs.py`: Any functions associated with the component.
- `opts.py`: Click command line options associated with the component. Defined here so they can be reused across the CLI. Eg. `--species` is used for multiple commands. The species CLI option is defined here and imported to all commands that use it.
- `enums.py`: Any enumerations associated with the component.
