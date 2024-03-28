"""Web based config editor"""

from dash import Dash
import dash_bootstrap_components as dbc

from src.components import layout

BOOTSTRAP_ICONS = (
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/" "font/bootstrap-icons.css"
)


def main() -> None:
    app = Dash(
        use_pages=True,
        pages_folder="./src/pages",
        external_stylesheets=[
            "./assets/stle.css",
            dbc.themes.BOOTSTRAP,
            BOOTSTRAP_ICONS,
        ],
        suppress_callback_exceptions=True,
    )
    app.title = "ConfigTree"
    app.layout = layout.render(
        app,
    )
    app.run(debug=True)


if __name__ == "__main__":
    main()
