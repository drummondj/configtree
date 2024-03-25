"""Web based config editor"""

from dash import Dash
import dash_bootstrap_components as dbc

from src.components import layout


def main() -> None:
    app = Dash(
        use_pages=True,
        pages_folder="./src/pages",
        external_stylesheets=[
            "./assets/stle.css",
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP,
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
