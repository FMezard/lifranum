import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import json

def read_blogposts(blogposts_files) :
    with open(blogposts_files, "r", encoding="utf-8") as file:
        blogposts = json.load(file)
    return blogposts

def main():
    read_blogposts("blogspot.json")

# app.layout = html.Div(children=[
#     html.H1(children='Annotation du corpus LIFRANUM'),
#     html.Div(children='''
#         Exploring data from Twitter
#     '''),
#     html.Label('Checkboxes'),
#     dcc.Checklist(id='my-input',
#         options=[
#             {'label': 'Ethos', 'value': 'ethos'},
#             {'label': u'Production', 'value': 'aut_num'},
#             {'label': 'Production sur twitter', 'value': 'prod_twitter'}
#         ],
#                   value=['ethos']
#
#
#     ),
#
#     dcc.Graph(
#         id='example-graph'),
#     html.Br(),
#     html.Div(id='my-output')
# ])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # app.run_server(debug=True)
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
