import click
from austrakka.utils.cmd_filter import hide_admin_cmds

from austrakka import __prog_name__ as PROG_NAME
from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_description, opt_document_file_name, opt_document_id, \
    opt_output_dir
from austrakka.components.project.document.funcs import add_document, enable_document, \
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
@click.option('-fp',
              '--file-path',
              help='Document to upload to the project.', required=True,)
@opt_description(required=True,
                 help="Brief description of document. ")
def document_add(
        project_abbrev: str,
        file_path: str,
        description: str):
    add_document(file_path, description, project_abbrev)    

@document.command(
    'download',
    help=f'Download a document within a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@opt_document_id()
@opt_output_dir()
def document_download(
    project_abbrev: str,
    document_id: int,
    output_dir: str
):
    download_document(project_abbrev, document_id, output_dir)

@document.command(
    'delete',
    help=f'Delete a document within a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@opt_document_id()
def document_delete(
    project_abbrev: str,
    document_id: int,
):
    disable_document(project_abbrev, document_id)

@document.command(
    'enable',
    help=f'Enable a document within a given project in {PROG_NAME}',
    hidden=hide_admin_cmds()
)
@click.argument('project-abbrev', type=str)
@opt_document_id()
def document_enable(
    project_abbrev: str,
    document_id: int,
):
    enable_document(project_abbrev, document_id)


@document.command(
    'update',
    help=f'Update a document within a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@opt_document_id()
@opt_document_file_name(required=False)
@opt_description(required=False, help="Brief description of document. ")
def document_update(
    project_abbrev: str,
    document_id: int,
    file_name: str,
    description: str
):
    update_document(project_abbrev, document_id, file_name, description)
