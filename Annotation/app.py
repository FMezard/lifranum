# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import json

from dash_html_template import Template

from pprint import pprint

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

def json_to_dict(blogposts_files) :
    # Returns a dict with the id of the post as keys
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


blogposts = json_to_dict("posts.json")

def get_blogs(blogposts):
    table_blogs = html.Table(
        children=[],
        id="table_blogs"
    )
    for k in blogposts:
        title = blogposts[k]["title"]
        if title == '':
            title = 'Sans Titre'
        tr_blog = html.Tr(children=[])
        tr_blog.children.append(html.Td(blogposts[k]["blog_id"]))
        tr_blog.children.append(html.Td(title))
        tr_blog.children.append(html.Td(blogposts[k]["url"]))
        tr_blog.children.append(html.Td(blogposts[k]["author_displayName"]))

        table_blogs.children.append(dcc.Link(tr_blog, href='display_post'))
    return table_blogs


@app.callback(
    Output(component_id='blogs', component_property='children'),
    Input(component_id='searchbox', component_property='value')
)
def filter_results(input_value):
    filtered_posts = list()
    for post in blogposts:
        # TODO Ajouter des .lowers
        if any([input_value in blogposts[post][k] for k in blogposts[post]]):
            filtered_posts.append(post)

    table_blogs = html.Table(
        children=[],
        id="table_blogs"
    )
    for i in filtered_posts:
        tr_blog = html.Tr(children=[])
        tr_blog.children.append(html.Td(dcc.Link(i, href=f'/{i}')))
        tr_blog.children.append(html.Td(blogposts[i]["title"]))
        tr_blog.children.append(html.Td(blogposts[i]["url"]))
        tr_blog.children.append(html.Td(blogposts[i]["author_displayName"]))
        table_blogs.children.append(tr_blog)
    return table_blogs

@app.callback(Output('post-content', 'children'),
              Input('url', 'pathname'))
def display_one_post(pathname):
    displayed_post = list(blogposts.keys())[0]
    if pathname:
        for blog in blogposts:
            if blog in pathname:
                displayed_post = blogposts[blog]
                break

        post = html.Div(children=[
            html.H2(displayed_post['title']),
            html.H2(displayed_post['author_displayName']),
            html.Div(["Labels choisis par l'éditeur : "]),
            html.Div(displayed_post['labels']),
            html.Div((Template.from_string(f'<div>{displayed_post["content"]}</div>')))

        ])
        return post



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
    html.Div(id='post-content')
])



if __name__ == '__main__':
    app.run_server(debug=True)
