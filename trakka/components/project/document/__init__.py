import click
from trakka.utils.cmd_filter import hide_admin_cmds

from trakka import __prog_name__ as PROG_NAME
from trakka.utils.output import table_format_option
from trakka.utils.options import opt_description, opt_name, opt_file, opt_identifier, \
    opt_output_dir
from trakka.components.project.document.funcs import add_document, enable_document, \
    get_document_list, download_document, disable_document, update_document

@click.group()
@click.pass_context
def document(ctx):
    """Commands to manage project documents"""
    ctx.context = ctx.parent.context

@document.command(
    'list',
    help=f'List of documents for a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@table_format_option()
def document_list(project_abbrev: str, out_format: str): 
    get_document_list(project_abbrev, out_format, show_disabled=False)

@document.command(
    'list-all',
    help=f'List all documents, including disabled, for a given project in {PROG_NAME}',
    hidden=hide_admin_cmds()
)
@click.argument('project-abbrev', type=str)
@table_format_option()
def document_list_all(project_abbrev: str, out_format: str):
    get_document_list(project_abbrev, out_format, show_disabled=True)

@document.command(
    'add',
    help=f'Upload a document to a project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@opt_file(help='File path of document to upload to the project.', required=True)
@opt_name(required=False, help='Name of the document without file extension.')
@opt_description(required=True, help="Brief description of the document.")
def document_add(
        project_abbrev: str,
        file: str,
        name: str,
        description: str):
    add_document(file, name, description, project_abbrev)    

@document.command(
    'download',
    help=f'Download a document within a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@opt_identifier(var_name="document_id", help="Identifier for a project document")
@opt_output_dir()
def document_download(
    project_abbrev: str,
    document_id: str,
    output_dir: str
):
    download_document(project_abbrev, document_id, output_dir)

@document.command(
    'disable',
    help=f'Disable a document within a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@opt_identifier(var_name="document_id", help="Identifier for a project document")
def document_disable(
    project_abbrev: str,
    document_id: str,
):
    disable_document(project_abbrev, document_id)

@document.command(
    'enable',
    help=f'Enable a document within a given project in {PROG_NAME}',
    hidden=hide_admin_cmds()
)
@click.argument('project-abbrev', type=str)
@opt_identifier(var_name="document_id", help="Identifier for a project document")
def document_enable(
    project_abbrev: str,
    document_id: str,
):
    enable_document(project_abbrev, document_id)


@document.command(
    'update',
    help=f'Update a document within a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@opt_identifier(var_name="document_id", help="Identifier for a project document")
@opt_name(required=False, help='Name of the document.')
@opt_description(required=False, help="Brief description of the document.")
def document_update(
    project_abbrev: str,
    document_id: str,
    file_name: str,
    description: str
):
    update_document(project_abbrev, document_id, file_name, description)
