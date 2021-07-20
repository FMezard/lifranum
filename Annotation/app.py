# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
import json

from dash_html_template import Template

from pprint import pprint

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
pd.set_option('display.max_colwidth', None)

def json_to_dict(blogposts_files) :
    # Returns a dict with the id of the post as keys
    # Fonction à adapter pour tjs avoir les données au bon format --> Sauf si on fait les requêtes au fur et à mesure
    # dans MongoDB mais je sais pas comment
    with open(blogposts_files, "r", encoding="utf-8") as file:
        blogposts = json.load(file)
        posts = {}
        for b in blogposts:
            title = b["title"]
            if b["title"] == "":
                title = "Sans Titre"

            posts[b["_id"]] = \
                {
                "blog_id": b["blog"]["id"],
                 "published": b["published"],
                 "updated" : b["updated"],
                 "url": b["url"],
                 "title": title,
                 "content": b["content"],
                 "labels": b["labels"],
                 "author_id": b["author"]["id"],
                 "author_displayName": b["author"]["displayName"]
            }
    return posts

def json_to_dataframe(blogposts_files) :
    with open(blogposts_files, "r", encoding="utf-8") as file:
        blogposts = json.load(file)
        # ajouter les auteurs des commentaires
        columns = ["blog_id", "published", "url", "title", "content", "labels", "author_id", "author_displayName", "updated"]
    dataframe = {}
    for c in columns:
        dataframe[c] = []
    for b in blogposts:
        title = b["title"]
        if b["title"] == "":
            title = "Sans Titre"

        dataframe["blog_id"].append(b["blog"]["id"])
        dataframe["published"].append(b["published"])
        dataframe["updated"].append(b.get("updated", ""))
        dataframe["url"].append(b["url"])
        dataframe["title"].append(title)
        dataframe["content"].append(b["content"])
        dataframe["labels"].append(b["labels"])
        dataframe["author_id"].append(b["author"]["id"])
        dataframe["author_displayName"].append(b["author"]["displayName"])
    df = pd.DataFrame(dataframe)
    return df



blogposts = json_to_dict("posts.json")
blogposts_df = json_to_dataframe("posts.json")
blogposts_df['id'] = blogposts_df.index




@app.callback(Output(component_id='post-content', component_property='children'),
              Input(component_id='table_blogs', component_property='selected_row_ids'))

def display_one_post(selected_row_ids):
    post = ""
    if selected_row_ids:

        dff = blogposts_df.loc[selected_row_ids]
        post = html.Div(id='post-content-child',
                 children=[
                     html.H2(dff['title']),
                     html.H3(dff['author_displayName']),
                     html.Div((Template.from_string(f'<div>{dff.iloc[0]["content"]}</div>')))
                 ])
    return post

@app.callback(
    Output(component_id='blogs', component_property='children'),
    Input(component_id='searchbox', component_property='value')
)
def filter_results(input_value):
    mask = np.column_stack([blogposts_df[col].str.contains(input_value, na=False) for col in blogposts_df.loc[:, blogposts_df.columns != 'id']])
    filtered_df = blogposts_df.loc[mask.any(axis=1)]
    table = dash_table.DataTable(
        id='table_blogs',
        filter_action='native',
        sort_action='native',
        row_selectable='single',
        columns=[{"name": "ID", "id": "blog_id"},
                 {"name": "Titre", "id": "title"},
                 {"name": "Mots-clés", "id": "labels"},
                 {"name": "Auteur.e", "id": "author_displayName"}
                 ],
        data=filtered_df.to_dict('records'))
    return table

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1(children='Lifranum Blogs Visualization'),
    dcc.Input(
        id="searchbox",
        type="text",
        placeholder="Search",
        value=""
    ),
    html.Div(id='blogs'),
    dash_table.DataTable(id='table_blogs'),
    html.Div(id="post-content")
])


if __name__ == '__main__':
    app.run_server(debug=True)
