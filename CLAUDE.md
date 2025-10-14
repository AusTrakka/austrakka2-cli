# Software Development Practices

## Structure
### Click commands
1. All public facing Click commands are placed in __init__.py and are declared with options and parameters. 
2. Command declarations don't do any work. Instead, they immediately call methods in the sibling funcs.py file.
3. The naming of command declaration functions are reversed in the top-level function in funcs.py. For example
   the command function might be declared as proforma_add(), and it would call add_proforma() in func.py to do
   the work.
4. Commands are organised under "<project-root>/austrakka/components/<component1>/__init__.py", and also func.py
   in the same directory. There may also be sub commands under each component directory.

### Tests
1. We favour writing end-to-end tests with no mocks. You can expect the environment to be set up for you
   to simply run these test.
2. All tests for each Click command are placed in the same file. One file per command.
3. Naming convention for the test file is "test_<command-name>_commands.py".
4. All end-to-end tests are placed in the "<project-root>/test/end_to_end_tests" folder.
5. Look at "<project-root>/test/end_to_end_tests/test_seq_add_commands.py" as the example for how tests are written.
6. Expect utilities to be available in ete_utils.py for creating data and invoking commands.
7. Tests are run using pytest.
8. One test should be written for each use case. That means one test per major assert (the point of the test).
   There can be other asserts of minor property values, those are fine, but do not test many error conditions
   that represent distinct use case, all in the one test.

### Running Tests
To run tests in this project, follow these steps:

   1. Ensure the following environment variables are set with your credentials:
       * AT_AUTH_TENANT_ID
       * AT_AUTH_APP_URI
       * AT_AUTH_PROCESS_ID
       * AT_AUTH_PROCESS_SECRET
	  
	  This can be achieved by running 'austrakka auth process' once, which will populate these variables
	  in your shell's current environment. Once you've done this the first time, then you must run it a
	  second time with 'export AT_TOKEN=$(austrakka auth process)' to populate the token before pytest
	  can run.

   2. Execute the tests using the following command, which handles authentication and runs pytest for a specific test suite:
   		pipenv run bash -c 'export AT_TOKEN=$(austrakka auth process) && pytest <path_to_test_file>'

	  or run all tests with:
		pipenv run bash -c 'export AT_TOKEN=$(austrakka auth process) && pytest'

### Linting
1. Linting is performed by running "pylint austrakka".
2. Always run the linter and fix any issues identified before commiting the code.

## Coding style
1. All private functions start with '_' and are positioned towards the bottom of the file.
2. Rather than specify Click options using raw constructs, custom options are normally created for reuse. For
   example, instead of annotating a function with:

  click.option(
        '-f',
        '--format',
        'out_format',
        default=default,
        type=click.Choice(valid_formats),
        help='Formatting option',
        show_default=True,
    )

   We instead wrap it up in a function and place it in the <project-root>/austrakka/utils/options.py file.
   Here's an example for a different option.

   def opt_group_name(var_name='group_name', **attrs: t.Any):
       defaults = {
           'required': True,
           'help': 'Group Name',
       }
       return create_option(
           "-g",
           "--group-name",
           var_name,
           type=click.STRING,
           **{**defaults, **attrs}
       )

	and then use it like this:

	@opt_group_name(var_name='group_names', multiple=True)
	def proforma_share(proforma_abbrev: str, group_names: List[str]):
		pass

