import dash
import dash_bootstrap_components as dbc
import dataframes
import pandas as pd
import os


def get_data():
    data = [dirname for dirname in os.listdir("Donnees")]

    posts = [f"{dirname}/blog_posts_{dirname}.json" for dirname in data]
    infos = [f"{dirname}/blog_info_{dirname}.json" for dirname in data]

    blogposts_df = dataframes.blogposts_dataframe(posts, type="posts")
    blogs_df = dataframes.blogposts_dataframe(infos, type="blog")
    blogposts_df['id'] = blogposts_df.index
    blogs_df['id'] = blogposts_df.index

    return (blogposts_df, blogs_df)


blogposts_df, blogs_df = get_data()
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
