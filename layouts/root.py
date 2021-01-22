import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from layouts import heatmap, list_view

# Top level layout
layout = dbc.Container(
    [
        dbc.Container(html.H1("Spotify Trend Explorer"), fluid=True),
        html.Hr(),  # Horizontal line
        dbc.Row(
            [
                dbc.Col(heatmap.layout, width=7, ),  # className='column_left'
                dbc.Col(list_view.layout, width=5, )
            ],
            no_gutters=True
        ),
        html.Hr(),  # Horizontal line
        dcc.Store(id='current_region', data=""),
        dcc.Store(id='selected_countries', data=""),
        dcc.Store(id='current_feature', data=""),
        dcc.Store(id='current_date'),
        dcc.Store(id='test'),
    ],
    fluid=True
)
