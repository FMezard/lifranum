import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import json

from dash_html_template import Template

# TODO : Mettre du css !

app = dash.Dash(__name__)
# external_stylesheets=external_stylesheets
def json_to_dict(blogposts_files) :
    with open(blogposts_files, "r", encoding="utf-8") as file:
        blogposts = json.load(file)
    return blogposts


blogspots = json_to_dict("blogspot.json")


def get_blogs(blogs):
    table_blogs = html.Table(
        children=[],
        id="table_blogs"
    )
    for i in range(1, len(blogs)):
        title = blogspots[i]["title"]
        if title == '':
            title = 'Sans Titre'
        tr_blog = html.Tr(children=[])
        tr_blog.children.append(html.Td(blogspots[0]["blog"]["id"]))
        tr_blog.children.append(html.Td(title))
        tr_blog.children.append(html.Td(blogspots[i]["url"]))
        tr_blog.children.append(html.Td(blogspots[i]["author"]["displayName"]))

        table_blogs.children.append(dcc.Link(tr_blog, href='display_post'))
    return table_blogs


@app.callback(
    Output(component_id='blogs', component_property='children'),
    Input(component_id='searchbox', component_property='value')
)
def filter_results(input_value):
    filtered_posts = list()
    for post in blogspots[1:]:
        if input_value in post["title"]:
            filtered_posts.append(post)
    table_blogs = html.Table(
        children=[],
        id="table_blogs"
    )
    for i in range(0, len(filtered_posts)):
        title = filtered_posts[i]["title"]
        if title == '':
            title = 'Sans Titre'
        tr_blog = html.Tr(children=[])
        tr_blog.children.append(html.Td(filtered_posts[0]["blog"]["id"]))
        tr_blog.children.append(html.Td(title))
        tr_blog.children.append(html.Td(filtered_posts[i]["url"]))
        tr_blog.children.append(html.Td(filtered_posts[i]["author"]["displayName"]))
        table_blogs.children.append(dcc.Link(tr_blog, href=f'/{filtered_posts[i]["_id"]}'))
    return table_blogs

# Je suis obligée de regarder les id de tous les posts, je dois pouvoir faire mieux !
@app.callback(Output('post-content', 'children'),
              Input('url', 'pathname'))
def display_one_post(pathname):
    post_content = blogspots[1]
    if pathname:
        for blog in blogspots[1:]:
            print(blog['_id'])

            if blog['_id'] in pathname:
                post_content = blog
                break

        post = html.Div(children=[
            html.H2(post_content['title']),
            html.H2(post_content['author']['displayName']),
            html.Div((Template.from_string(f'<div>{post_content["content"]}</div>')))

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
