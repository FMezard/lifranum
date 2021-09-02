from main_dash import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

def make_layout():
    return html.Div(children=[html.Header(children=[
        dcc.Location(id='url', refresh=False),
        dbc.Container(children=[
            dbc.Row(className="menu", children=[
                dbc.Col(children=[html.Img(src=app.get_asset_url('lifranum.jpg'), alt="logo Lifranum", width="120px", className="logo")],
                        className="col-2"),
                dbc.Col(children=[html.H1(children='Blogspot')], className="col-3"),
                dbc.Col(dcc.Link(id="button_authors", className="col-12", children=['Auteurs'], href="/authors")),
                dbc.Col(dcc.Link(id="button_posts", className="col-12", children=['Posts de blogs'], href="/posts")),
                dbc.Col(dcc.Link(id="button_blogs", className="col-12", children=['Blogs'], href="blogs"))])])]),
        html.Div(id='content')]

    )
