from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import WIDGET_PATH


@logger_wraps()
def add_widget(name: str):
    """
    Add a widget for later inclusion in a dashboard.
    """
    api_post(
        path=WIDGET_PATH,
        data={
            "name": name
        }
    )


@logger_wraps()
def update_widget(widget_id: int, new_name: str):
    """
    Update an existing widget.
    """
    api_put(
        path=f'{WIDGET_PATH}/{widget_id}',
        data={
            "name": new_name
        }
    )


@logger_wraps()
def list_widgets(out_format: str):
    """
    List widgets available for inclusion in a dashboard.
    """
    call_get_and_print(WIDGET_PATH, out_format)


@logger_wraps()
def get_widget(widget_id: int, out_format: str):
    """
    List widgets available for inclusion in a dashboard.
    """
    full_path = f'{WIDGET_PATH}/{widget_id}'
    call_get_and_print(full_path, out_format)
