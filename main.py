""" Main file. Collects the app and holds all callback functions.
"""
import dash
from dash.dependencies import Input, Output, State
import time

from utility.file_loading import *
from layouts import root, heatmap, list_view
from layouts.list_view import *
from colors.colordicts import master_dict, af_value_range_dict

# Set bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Loading data
data_path_main = os.path.join(os.path.dirname(__file__), 'data', '')
data_path_audio_features = os.path.join(data_path_main, '20201026_data', '')  # 4 year data-set

regions = ['DNK',
           'ARG',
           'AUS',
           'AUT',
           'BEL',
           'BGR',
           'BOL',
           'BRA',
           'CAN',
           'CHE',
           'CHL',
           'COL',
           'CRI',
           'CYP',
           'CZE',
           'DEU',
           'DOM',
           'ECU',
           'ESP',
           'EST',
           'FIN',
           'FRA',
           'GBR',
           'GRC',
           'GTM',
           'HKG',
           'HND',
           'HUN',
           'IDN',
           'IRL',
           'ISL',
           'ISR',
           'ITA',
           'JPN',
           'LTU',
           'LUX',
           'LVA',
           'MEX',
           'MYS',
           'NIC',
           'NLD',
           'NOR',
           'NZL',
           'PAN',
           'PER',
           'PHL',
           'POL',
           'PRT',
           'PRY',
           'ROU',
           'SGP',
           'SLV',
           'SVK',
           'SWE',
           'THA',
           'TUR',
           'TWN',
           'URY',
           'USA',
           'VNM',
           ]  # Regions of interest
# regions = ['DNK', 'GBR']  # Regions of interest

data = load_files(data_path_audio_features, regions, None, True)
# add column with data in seconds instead of milli-seconds
data['duration_s'] = data['duration_ms'] / 1000
data_mean = create_mean_vectors(data)
dates = create_unique_dates(data)
years = dates.year.unique().sort_values()

# Creating layout
app.layout = root.layout

available_audio_features = ["tempo",
                            "energy",
                            "acousticness",
                            "liveness",
                            "speechiness",
                            "valence",
                            "duration_s",
                            "danceability",
                            "loudness",
                            "instrumentalness"]


# Callback functions
@app.callback(
    [Output('view_heatmap', 'figure'),
     Output('current_date', 'data'),
     Output('current_region', 'data'),
     Output('current_feature', 'data'),
     ],
    [Input('heatmap_country_dropdown', 'value'),
     Input('heatmap_audio_feature_dropdown', 'value'),
     Input('list_view', 'data'),
     Input('tableclick', 'data'),
     Input('view_heatmap', 'clickData'),
     Input('metric_dropdown', 'value'),
     Input('radioitems_color', 'value')
     ],
    [State('current_date', 'data'),
     State('current_region', 'data'),
     State('current_feature', 'data'), ]
)
def callback_update_heatmap(selected_countries, selected_audio_features, table_data, selected_row, heatmap_click_data,
                            metric, radio_selected_colordict,
                            current_date, current_region, current_feature):
    """ Updates heatmap when changes is made to the dropdown menus
    """
    selected_region = current_region
    selected_feature = current_feature
    selected_date = datetime.now()

    n_audio_features = len(selected_audio_features)
    n_countries = len(selected_countries)

    # Decide on color dict
    af_to_color_dict = master_dict[radio_selected_colordict]

    if ((selected_row is not None) and (table_data != [])):

        # Get selected song
        row_id = selected_row
        selected_song = next((item for item in table_data if item['id'] == row_id), None)

        # Get selected song
        # selected_song = table_data[selected_row]

        # Find occurences of songs
        song_occurences = get_subset(data, {
            "Track Name": [selected_song["Track Name"]],
            "Artist": [selected_song["Artist"]],
            "region": selected_countries
        })[['date', 'region', 'Position']]  # Extract only date and region

        # occurence_dates = song_occurences['date']
        # occurence_dates = pd.to_datetime(occurence_dates, dayfirst=True)
        fig = heatmap.create_heatmap_subset_figure(data_mean, dates, selected_countries, selected_audio_features,
                                                   metric, af_value_range_dict, af_to_color_dict,
                                                   song_occurences)

        heatmap.add_white_space_between_audio_features(fig, dates, n_countries, n_audio_features)
        heatmap.add_chart_position(fig, song_occurences, selected_countries, selected_audio_features, dates)
    else:
        fig = heatmap.create_heatmap_figure(data_mean, dates, selected_countries, selected_audio_features, metric,
                                            af_value_range_dict, af_to_color_dict)

        heatmap.add_white_space_between_audio_features(fig, dates, n_countries, n_audio_features)

    if heatmap_click_data is not None:

        # If callback is triggered by change in dropdowns, update bounding box accordingly
        ctx = dash.callback_context
        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if (trigger_id == 'heatmap_country_dropdown'):
                # Check if currently selected country is still in selected countries
                if current_region in selected_countries:
                    # Find y-coordinate in another fashion
                    heatmap_y_coord = heatmap.country_feature_to_yval(selected_countries, selected_audio_features,
                                                                      country=current_region)
                    selected_region = current_region
                else:
                    return [fig, selected_date, selected_region, current_feature]
            elif (trigger_id == 'heatmap_audio_feature_dropdown'):
                # Check if currently selected feature is still in selected features
                if current_feature in selected_audio_features:
                    # Find y-coordinate in another fashion
                    heatmap_y_coord = heatmap.country_feature_to_yval(selected_countries, selected_audio_features,
                                                                      feature=current_feature)
                    selected_feature = current_feature
                else:
                    asdasdasd = 1  # Do nothing
                    # return [fig, selected_date, current_region, selected_feature]
            else:
                heatmap_y_coord = heatmap_click_data['points'][0]['y']

                # Extract region from heatmap_click_data
                [selected_region, selected_feature] = heatmap.yval_to_country_feature(heatmap_y_coord,
                                                                                      selected_countries,
                                                                                      selected_audio_features)

        # Extract date from heatmap_click_data
        selected_date = heatmap_click_data['points'][0]['x']
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')

        # Extract what rows to mark
        # Extract y-coordinates
        # y_coord = heatmap_click_data['points'][0]['y']

        # If callback is triggered by click on heatmap, calculate country_no based on clicked heatmap y coordinate
        ctx = dash.callback_context
        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if (trigger_id == 'view_heatmap'):
                country_no = heatmap_y_coord % n_countries
            else:
                # If not triggered by click on heatmap, find country_no based on occurence of country name in the list of selected countries
                country_no = selected_countries.index(current_region)
                selected_region = current_region

        heatmap.add_white_space_between_audio_features(fig, dates, n_countries, n_audio_features)

        for i in range(0, n_audio_features):
            row = n_countries * i + country_no
            heatmap.add_bounding_box_to_heatmap(fig, selected_date, row, row)

        #
        # row_min = country_y_coord - (country_y_coord % n_audio_features)
        # row_max = row_min + n_audio_features - 1
        #
        # heatmap.add_bounding_box_to_heatmap(fig, selected_date, row_min, row_max)

    return [fig, selected_date.strftime("%Y-%m-%d"), selected_region, selected_feature]


@app.callback(
    [
        Output('list_view', 'columns'),
    ],
    [
        Input('heatmap_audio_feature_dropdown', 'value'),
    ]
)
def callback_update_list_view_columns(selected_audio_features):
    """ Updates the columns of list view when audio features are selected or deselected
    :param selected_audio_features:
    :return:
    """
    # print("callback_update_list_view_columns called.")

    selected_audio_features = np.asarray([selected_audio_features]).flatten()
    columns = [
        {'id': 'Position', 'name': 'Pos.'},
        {'id': 'Track Name', 'name': 'Song'},
        {'id': 'Artist', 'name': 'Artist'}
    ]

    for af in selected_audio_features:
        columns.append({"id": af,
                        "name": heatmap.dict_col_name_to_label_name[af],
                        'type': 'numeric',
                        'format': {
                            'specifier': '.4f',
                        }
                        })

    return [columns]


@app.callback(
    [
        Output('list_view', 'data'),
        Output('list_view', 'style_data_conditional'),
        Output('list_view', 'selected_rows'),
        Output("label_list_view_week_region", "children"),
        Output('tableclick', 'data'),
    ],
    [
        Input('view_heatmap', 'clickData'),
        Input('list_view', 'active_cell'),
        Input('heatmap_country_dropdown', 'value'),
        Input('radioitems_color', 'value'),
    ],
    [
        State('heatmap_audio_feature_dropdown', 'value'),
        State('tableclick', 'data'),
        State('current_date', 'data'),
        State('current_region', 'data'),
        State('list_view', 'style_data_conditional'),
    ]
)
def callback_update_list_view_data(clickedData, active_cell, heatmap_selected_countries, radio_selected_colordict,
                                   heatmap_selected_afs, prev_row,
                                   prev_date, prev_region, prev_style):
    # If callback is triggered by change in country dropdown and the previously selected country is not in
    # the list of currently selected countries, empty list
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if (trigger_id == 'heatmap_country_dropdown'):
            if prev_region not in heatmap_selected_countries:
                return [pd.DataFrame().to_dict('rows'), dash.no_update, [], dash.no_update, []]

    list_view_selected_rows = []
    tableclick_active_row = []
    styles = []

    # Decide on color dict
    af_to_color_dict = master_dict[radio_selected_colordict]

    # Remove pink selection
    # Source: https://stackoverflow.com/questions/56363437/disable-highlighting-of-active-cell-in-dashtable
    styles.extend([{
        "if": {"state": "selected"},
        "backgroundColor": list_view_row_selected_color,
        "border": "inherit !important",
    }])

    if active_cell is not None:
        # tableclick_active_row = active_cell["row"]
        tableclick_active_row = active_cell["row_id"]

    if clickedData is None:
        return dash.no_update  # ignore the call

    n_features_to_track = len(heatmap_selected_afs)

    dataPoint = clickedData['points']

    # Extract date
    date = dataPoint[0]['x']
    # date = datetime.strptime(date, '%Y-%m-%d')

    # Extract region

    # If callback is triggered by clicking on the heatmap, get the region of the clicked bin.
    # Otherwise, use previously selected region
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if (trigger_id == 'view_heatmap'):
            yval = dataPoint[0]['y']
            [region, af] = heatmap.yval_to_country_feature(yval, heatmap_selected_countries, heatmap_selected_afs)
        else:
            region = prev_region

    # data_filtered = get_subset(data, {"date": [date], "region": [region]})
    data_filtered = get_subset(data, {"region": [region], "date": [date]})

    date_formatted = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B %Y')

    for af in available_audio_features:
        (style, legend_tempo) = discrete_background_color_bins(data_filtered, af_value_range_dict, af_to_color_dict,
                                                               columns=[af])
        styles.extend(style)

    label_text = region + " - " + date_formatted

    # Check whether a new region/date was selected
    if (region == prev_region) & (date == prev_date):
        new_region_or_date_selected = False
    else:
        new_region_or_date_selected = True

    # For highlighting entire rows and allowing for the possibility of unselecting
    # Source: https://stackoverflow.com/questions/63156919/unselect-active-cell-in-dash-datatable-python
    if active_cell is None:
        if (prev_row is None) | new_region_or_date_selected:
            # This triggers when a new region or date is selected
            tableclick_active_row = None
            # return [{}], None, []
        else:
            tableclick_active_row = prev_row
            # Reuse old style style
            styles = prev_style
    elif "row" in active_cell:
        if active_cell.get("row_id", "") == prev_row:
            # This triggers when a row is unselected
            tableclick_active_row = None
            list_view_selected_rows = []
            print("Row {} unselected.".format(prev_row))
        else:
            # This triggers when a row is selected
            # tableclick_active_row = active_cell.get("row", "")
            tableclick_active_row = active_cell["row_id"]
            list_view_selected_rows = [active_cell["row"]]
            print("Row {} selected.".format(tableclick_active_row))
            style = [{
                "if": {"row_index": active_cell.get("row", "")},
                "backgroundColor": list_view.list_view_row_selected_color,
            }]
            styles.extend(style)

    return [data_filtered.to_dict('rows'), styles, list_view_selected_rows, label_text, tableclick_active_row]


@app.callback(
    Output('spotify_player', 'src'),
    [Input('tableclick', 'data')],
    [State('list_view', 'data')]
)
def callback_spotify_player(row_id, table_data):
    if row_id is None:
        return dash.no_update  # ignore the call

    if len(row_id) < 1:
        return dash.no_update  # ignore the call

    # Get selected song
    selected_song = next((item for item in table_data if item['id'] == row_id), None)
    # Extract track ID
    track_id = selected_song['track_id']

    return "https://open.spotify.com/embed/track/" + track_id


"""
@app.callback(
    Output('heatmap_country_dropdown', 'value'),
    [Input('tree_view', 'checked')],
    State('heatmap_country_dropdown', 'value')
)
def callback_update_selected_countries_from_tree(tree_countries, dropdown_countries):
    world_parts = [t for t in tree_countries if t[0] == "_"]
    regions = [t for t in tree_countries if t[0] != "_"]
    print(regions)

    if regions == dropdown_countries:
        return dash.no_update
    else:
        return regions
"""

"""
@app.callback(
    [Output('tree_view', 'checked')],
    [Input('heatmap_country_dropdown', 'value')],
    State('tree_view', 'checked')
)
def update_tree_from_selected_countries(dropdown_countries, tree_countries):

    world_parts = [t for t in tree_countries if t[0] == "_"]
    regions = [t for t in tree_countries if t[0] != "_"]

    if regions == dropdown_countries:
        return dash.no_update
    else:
        # return dropdown_countries
        return ['NZL']
        """


# Is triggered by changing the dcc.storage "tableclick"
# resets active cell and selected cell via callback below
@app.callback([Output('loopbreaker_div', "children")], [Input('tableclick', 'data')])
def reset_active_cell(input=None):
    return [html.Div(id='loopbreaker', children=True)]


# For highlighting entire rows and allowing for the possibility of unselecting
# Source: https://stackoverflow.com/questions/63156919/unselect-active-cell-in-dash-datatable-python
# loopbreaker to avoid circular dependency
@app.callback([Output('list_view', "active_cell"), Output('list_view', 'selected_cells')],
              [Input('loopbreaker', 'children')])
def reset_active_cell(input=None):
    time.sleep(1)
    return (None, [])


def main():
    app.run_server(debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
