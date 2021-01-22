import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.express as px
import colorlover

from utility.data_filtering import *
import plotly.graph_objects as go
from utility.data_processing import *
from dash_table import DataTable
from colors.colormaps import get_colormap_rgb

list_view_row_selected_color = "rgba(146, 192, 234, 0.5)"

spotify_player = html.Iframe(id='spotify_player',
                             src="https://open.spotify.com/embed/track/3cGmXmTH6cUW2vCKWehmBp",
                             width="300",
                             height="80",
                             )

start_table_df = pd.DataFrame(columns=[''])

# Layout of list view
layout = dbc.Container(
    [
        html.H2("Top 200 chart", id='list_view_header'),  # style = {'textAlign' : 'center'}
        dcc.Store(id='tableclick'),
        html.Div(id='loopbreaker_div', children=[
            html.Div(id='loopbreaker', children=True)
        ]),

        html.Label("Select a week on the heatmap", id='label_list_view_week_region', style={'font-weight': 'bold'}),

        DataTable(id='list_view',
                  fixed_rows={'headers': True, 'data': 0},
                  data=start_table_df.to_dict('records'),
                  columns=[],
                  sort_action='native',
                  # filter_action='native',
                  # cell_selectable=True,
                  style_table={
                      'height': 550,
                      'overflowY': 'scroll',
                      'border': '1px solid grey'
                  },
                  style_cell={
                      'overflow': 'hidden',
                      'textOverflow': 'ellipsis',
                      'minWidth': '30px', 'width': '30px', 'maxWidth': '30px',
                      'textAlign': 'right',
                  },

                  style_cell_conditional=[
                      {
                          'if': {'column_id': 'Position'},
                          'textAlign': 'center',
                          'width': '10%'
                      },
                      {
                          'if': {'column_id': 'Track Name'},
                          'width': '30%',
                          'overflow': 'hidden',
                          'textOverflow': 'ellipsis',
                      },
                      {
                          'if': {'column_id': 'Artist'},
                          'width': '20%',
                          'overflow': 'hidden',
                          'textOverflow': 'ellipsis',
                      },
                      {
                          'if': {'column_id': 'Artist'},
                          'width': '20%',
                          'overflow': 'hidden',
                          'textOverflow': 'ellipsis',
                      },
                  ],
                  ),
        dbc.Row(dbc.Col(html.Label(" "), )),  # Filler
        dbc.Row(dbc.Col(html.Label(" "), )),  # Filler
        dbc.Row(dbc.Col(spotify_player)),
    ]
)


def discrete_background_color_bins(df, af_value_range_dict, af_to_color_dict, n_bins=100, columns='all'):
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]

    column_bounds = af_value_range_dict[columns[0]]
    df_min = column_bounds[0]
    df_max = column_bounds[1]
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]

    # Define color scale for this audio feature
    color_scale_fine = get_colormap_rgb(af_to_color_dict[columns[0]], n_bins)

    styles = []
    legend = []

    for i in range(1, len(bounds)):
        if i == 1:
            min_bound = -9999999999999
        else:
            min_bound = ranges[i - 1]
        if i == len(bounds):
            max_bound = 9999999999999
        else:
            max_bound = ranges[i]
        backgroundColor = color_scale_fine[i - 1]

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                            '{{{column}}} >= {min_bound}' +
                            (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': text_contrast_color(backgroundColor),  # text color,
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))


def text_contrast_color(bg_color):
    """ Decides if text should be black or white based on background luminance

    :param bg_color: RGB color
    :return:
    """
    bg_color_numeric = colorlover.to_numeric([bg_color])[0]

    # Computing luminance
    p_luminance = (0.299 * bg_color_numeric[0] + 0.587 * bg_color_numeric[1] + 0.114 * bg_color_numeric[2]) / 255;

    if (p_luminance > 0.6):
        text_color = 'black'
    else:
        text_color = 'white'

    return text_color
