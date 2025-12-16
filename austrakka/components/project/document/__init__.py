import click

from austrakka import __prog_name__ as PROG_NAME
from austrakka.utils.output import table_format_option
from austrakka.utils.options import opt_description, opt_document_id, opt_output_dir
from austrakka.components.project.document.funcs import add_document, \
    get_document_list, download_document, delete_document

# ADD*: Upload a document to project (path, project abbrev)
# LIST: List all documents present in a project
# DOWNLOAD: Download a document (project abbrev, document name, optional out path)
# INFO: Show metadata for a give document 
# DELETE*: Delete document in a project
# DISABLE*: Visibility toggle (don't delete but hide)
# ENABLE*: Visibility toggle (show)

@click.group()
@click.pass_context
def document(ctx):
    """Commands to manage project documents"""
    ctx.context = ctx.parent.context

@document.command(
    'add',
    help=f'Upload a document to a project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@click.option('-fp',
              '--file-path',
              help='Document to upload to the project.')
@opt_description(required=True,
                 help="Brief description of document. ")
def document_add(
        project_abbrev: str,
        file_path: str,
        description: str):
    add_document(file_path, description, project_abbrev)


@document.command(
    'list',
    help=f'Get a list of documents for a given project in {PROG_NAME}',
)
@click.argument('project-abbrev', type=str)
@table_format_option()
def document_list(project_abbrev: str, out_format: str):
    get_document_list(project_abbrev, out_format)


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
    delete_document(project_abbrev, document_id)