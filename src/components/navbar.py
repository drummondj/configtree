import dash_bootstrap_components as dbc
import dash
from dash import Dash, html


class PageNotFoundException(Exception):
    """Exception raised if a page is not found.

    Attributes:
        page -- name of missing page
    """

    def __init__(self, page):
        self.page = page
        self.message = f"code for page '{page}' not found in pages dir"
        super().__init__(self.message)


def render() -> dbc.NavbarSimple:
    pages = dash.page_registry.values()
    editor = next((page for page in pages if page["name"] == "Editor"), None)
    if not editor:
        raise PageNotFoundException("Editor")

    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    f" {editor['name']}",
                    href=editor["relative_path"],
                    class_name="bi bi-pencil-square",
                    active="exact",
                )
            )
        ],
        brand="ConfigTree",
        brand_href="/",
        color="dark",
        dark=True,
        links_left=True,
    )
