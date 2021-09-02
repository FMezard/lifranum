# -*- coding: utf-8 -*-
import dataframes
import html_parser
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import json
from main_dash import blogs_df, blogposts_df
from dash_html_template import Template

# import posts
# import blogs


from main_dash import app
from first_view import make_layout






# pd.set_option('display.max_colwidth', None)
app.layout = make_layout()
index_page = html.Div(id="main")
blogs_layout = html.Div(children=[
    dash_table.DataTable(
            id="table_blogs",
            style_cell={
            'text-align': 'left',
            'minWidth': 50,
            'maxWidth': 300,
            'whiteSpace': 'normal',
            'height': 'auto',
            },

        style_cell_conditional=[{

                'if': {
                    'column_id': 'name',
                },
                'text-align': 'left',
                'width' : '100'

        }, {
            'if': {
                'column_id': 'description',
            },
            'text-align': 'left',
            'width': '200'
        }],

            filter_action='native',
            sort_action='native',
            page_current=0,
            page_size=50,
            virtualization=True,
            page_action='none',
            row_selectable='single',

            columns=[{"name": "Titre", "id": "name"},
                     {"name": "Description", "id": "description"},
                     {"name": "Dernière publication", "id": "updated"},
                     {"name": "Création", "id": "published"}
                     ],

            data=blogs_df.to_dict('records')),
            html.Div(id="blog_content")])


blogpost_layout = html.Div(children=[
    dash_table.DataTable(
            id="table_posts",
            style_cell={
            'text-align': 'left'
            },

        style_cell_conditional=[{

                'if': {
                    'column_id': 'title',
                },
                'text-align': 'left',
                'width': '200px',
        },{
                'if': {
                        'column_id': 'labels',
                },
                'width': '200px',
    }],

            filter_action='native',
            sort_action='native',
            page_current=0,
            page_size=100,
            virtualization=True,
            page_action='none',
            row_selectable='single',

            columns=[{"name": "ID", "id": "blog_id"},
                     {"name": "Titre", "id": "title"},
                     {"name": "Mots-clés", "id": "labels"},
                     {"name": "Auteur.e", "id": "author_displayName"}
                     ],

            data=blogposts_df.to_dict('records')),
            html.Div(id="post_content")])


@app.callback(dash.dependencies.Output('content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/blogs':
        return blogs_layout
    elif pathname == '/posts':
         return blogpost_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here
#
#
@app.callback(Output(component_id='blog_content', component_property='children'),
              Input(component_id='table_blogs', component_property='selected_row_ids'))
def display_one_blog_info(selected_row_ids):
    post = ""
    if selected_row_ids:
        blog_row = blogs_df.loc[selected_row_ids[0], :]
        post = html.Div(id='blog-content-child',
                        children=[
                            html.Div(children=[html.Div(children='Nom du blog : ',className="categorie"), blog_row["name"]]),
                            html.Div(children=[html.Div(children="Description du blog : ",className="categorie"), blog_row['description']]),
                            html.Div(children=[html.Div(children="URL : ", className="categorie"),
                                               blog_row['url']]),

                            html.Div(children=[html.Div(children="Pays de l'auteur.ice",className="categorie"), blog_row['country']]),
                            html.Div(children=[html.Div(children="Langue du blog", className="categorie"),
                                               blog_row['language']]),
                            html.Div(children=[html.Div(children="Nombre total de postes", className="categorie"),
                                               blog_row['posts_total_items']])]
                        )
    return post

@app.callback(Output(component_id='post_content', component_property='children'),
              Input(component_id='table_posts', component_property='selected_row_ids'))
def display_one_post(selected_row_ids):
    post = ""
    print(selected_row_ids)
    if selected_row_ids:
        dff = blogposts_df.loc[selected_row_ids]
        post = html.Div(id='post-content-child',
                        children=[
                            html.H2(dff['title']),
                            html.H3(dff['author_displayName'], ),
                            html.Div(html_parser.html_to_dash(f"""<div>{dff.iloc[0]["content"]}</div>"""))
                            # html.Div(Template.from_string(f'<div>{dff.iloc[0]["content"]}</div>'), style={"text-align": "center"})
                        ],
                        )
    return post




if __name__ == '__main__':
    app.run_server(debug=True)



