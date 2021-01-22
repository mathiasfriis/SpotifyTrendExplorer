import datetime

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_treeview_antd
import plotly.graph_objects as go
import numpy as np
import itertools
from utility.data_filtering import *
from colors.colormaps import get_colormap_rgb
from colors.colordicts import *

# Dictionary for mapping column names to label names
dict_col_name_to_label_name = {'danceability': 'Danceability',
                               'valence': 'Valence',
                               'energy': 'Energy',
                               'liveness': 'Liveness',
                               'loudness': 'Loudness[dB]',
                               'speechiness': 'Speechiness',
                               'acousticness': 'Acousticness',
                               'instrumentalness': 'Instrumentalness',
                               'tempo': 'Tempo[BPM]',
                               'duration_ms': 'Duration[ms]',
                               'duration_s': 'Duration[s]',
                               }

# Layout of row where countries are chosen
countries_input = dbc.FormGroup(
    [
        # dbc.Label("Countries:", width=1),
        html.Div("Countries:", style={'width': '115px'}),
        dbc.Col(
            dcc.Dropdown(
                id='heatmap_country_dropdown',
                options=[
                    {'label': 'Argentina (ARG)', 'value': 'ARG'},
                    {'label': 'Australia (AUS)', 'value': 'AUS'},
                    {'label': 'Austria (AUT)', 'value': 'AUT'},
                    {'label': 'Belgium (BEL)', 'value': 'BEL'},
                    {'label': 'Bulgaria (BGR)', 'value': 'BGR'},
                    {'label': 'Bolivia (BOL)', 'value': 'BOL'},
                    {'label': 'Brazil (BRA)', 'value': 'BRA'},
                    {'label': 'Canada (CAN)', 'value': 'CAN'},
                    {'label': 'Switzerland (CHE)', 'value': 'CHE'},
                    {'label': 'Chile (CHL)', 'value': 'CHL'},
                    {'label': 'Colombia (COL)', 'value': 'COL'},
                    {'label': 'Costa Rica (CRI)', 'value': 'CRI'},
                    {'label': 'Cyprus (CYP)', 'value': 'CYP'},
                    {'label': 'Czechia (CZE)', 'value': 'CZE'},
                    {'label': 'Germany (DEU)', 'value': 'DEU'},
                    {'label': 'Denmark (DNK)', 'value': 'DNK'},
                    {'label': 'Dominican Republic (DOM)', 'value': 'DOM'},
                    {'label': 'Ecuador (ECU)', 'value': 'ECU'},
                    {'label': 'Spain (ESP)', 'value': 'ESP'},
                    {'label': 'Estonia (EST)', 'value': 'EST'},
                    {'label': 'Finland (FIN)', 'value': 'FIN'},
                    {'label': 'France (FRA)', 'value': 'FRA'},
                    {'label': 'United Kingdom (GBR)', 'value': 'GBR'},
                    {'label': 'Greece (GRC)', 'value': 'GRC'},
                    {'label': 'Guatemala (GTM)', 'value': 'GTM'},
                    {'label': 'Hong Kong (HKG)', 'value': 'HKG'},
                    {'label': 'Honduras (HND)', 'value': 'HND'},
                    {'label': 'Hungary (HUN)', 'value': 'HUN'},
                    {'label': 'Indonesia (IDN)', 'value': 'IDN'},
                    {'label': 'Ireland (IRL)', 'value': 'IRL'},
                    {'label': 'Iceland (ISL)', 'value': 'ISL'},
                    {'label': 'Israel (ISR)', 'value': 'ISR'},
                    {'label': 'Italy (ITA)', 'value': 'ITA'},
                    {'label': 'Japan (JPN)', 'value': 'JPN'},
                    {'label': 'Lithuania (LTU)', 'value': 'LTU'},
                    {'label': 'Luxembourg (LUX)', 'value': 'LUX'},
                    {'label': 'Latvia (LVA)', 'value': 'LVA'},
                    {'label': 'Mexico (MEX)', 'value': 'MEX'},
                    {'label': 'Malaysia (MYS)', 'value': 'MYS'},
                    {'label': 'Nicaragua (NIC)', 'value': 'NIC'},
                    {'label': 'Netherlands (NLD)', 'value': 'NLD'},
                    {'label': 'Norway (NOR)', 'value': 'NOR'},
                    {'label': 'New Zealand (NZL)', 'value': 'NZL'},
                    {'label': 'Panama (PAN)', 'value': 'PAN'},
                    {'label': 'Peru (PER)', 'value': 'PER'},
                    {'label': 'Philippines (PHL)', 'value': 'PHL'},
                    {'label': 'Poland (POL)', 'value': 'POL'},
                    {'label': 'Portugal (PRT)', 'value': 'PRT'},
                    {'label': 'Paraguay (PRY)', 'value': 'PRY'},
                    {'label': 'Romania (ROU)', 'value': 'ROU'},
                    {'label': 'Singapore (SGP)', 'value': 'SGP'},
                    {'label': 'El Salvador (SLV)', 'value': 'SLV'},
                    {'label': 'Slovakia (SVK)', 'value': 'SVK'},
                    {'label': 'Sweden (SWE)', 'value': 'SWE'},
                    {'label': 'Thailand (THA)', 'value': 'THA'},
                    {'label': 'Turkey (TUR)', 'value': 'TUR'},
                    {'label': 'Taiwan (TWN)', 'value': 'TWN'},
                    {'label': 'Uruguay (URY)', 'value': 'URY'},
                    {'label': 'United States of America (USA)', 'value': 'USA'},
                    {'label': 'Vietnam (VNM)', 'value': 'VNM'},
                ],
                value=['BRA', 'ARG', 'DNK', ],
                multi=True,
            ),
        )
    ],
    row=True
)

# Layout of row where audio feature is chosen
tree_view = html.Div([
    dash_treeview_antd.TreeView(
        id='tree_view',
        multiple=True,
        checkable=True,
        checked=['DNK', "AUS"],
        selected=[],
        expanded=['_all'],
        data={
            'title': 'All',
            'key': '_all',
            'children': [

                # EUROPE
                {
                    'title': 'Europe',
                    'key': '_europe',
                    'children': [
                        {'title': 'Austria', 'key': 'AUT'},
                        {'title': 'Belgium', 'key': 'BEL'},
                        {'title': 'Bulgaria', 'key': 'BGR'},
                        {'title': 'Switzerland', 'key': 'CHE'},
                        {'title': 'Cyprus', 'key': 'CYP'},
                        {'title': 'Czechia', 'key': 'CZE'},
                        {'title': 'Germany', 'key': 'DEU'},
                        {'title': 'Denmark', 'key': 'DNK'},
                        {'title': 'Spain', 'key': 'ESP'},
                        {'title': 'Estonia', 'key': 'EST'},
                        {'title': 'Finland', 'key': 'FIN'},
                        {'title': 'France', 'key': 'FRA'},
                        {'title': 'United Kingdom', 'key': 'GBR'},
                        {'title': 'Greece', 'key': 'GRC'},
                        {'title': 'Hungary', 'key': 'HUN'},
                        {'title': 'Ireland', 'key': 'IRL'},
                        {'title': 'Italy', 'key': 'ITA'},
                        {'title': 'Lithuania', 'key': 'LTU'},
                        {'title': 'Luxembourg', 'key': 'LUX'},
                        {'title': 'Latvia', 'key': 'LVA'},
                        {'title': 'Netherlands', 'key': 'NLD'},
                        {'title': 'Norway', 'key': 'NOR'},
                        {'title': 'Poland', 'key': 'POL'},
                        {'title': 'Portugal', 'key': 'PRT'},
                        {'title': 'Romania', 'key': 'ROU'},
                        {'title': 'Slovakia', 'key': 'SVK'},
                        {'title': 'Sweden', 'key': 'SWE'},

                    ],
                },

                # MIDDLE EAST
                {
                    'title': 'Middle East',
                    'key': '_middle_east',
                    'children': [
                        {'title': 'Israel', 'key': 'ISR'},
                        {'title': 'Turkey', 'key': 'TUR'},
                    ],
                },

                # OCEANIA
                {
                    'title': 'Oceania',
                    'key': '_oceania',
                    'children': [
                        {'title': 'Australia', 'key': 'AUS'},
                        {'title': 'New Zealand', 'key': 'NZL'},
                    ],
                },

                # NORTH AMERICA
                {
                    'title': 'North America',
                    'key': '_north_america',
                    'children': [
                        {'title': 'Canada', 'key': 'CAN'},
                        {'title': 'Dominican Republic', 'key': 'DOM'},
                        {'title': 'United States of America', 'key': 'USA'},
                    ],
                },

                # CENTRAL AMERICA
                {
                    'title': 'Central America',
                    'key': '_central_america',
                    'children': [
                        {'title': 'Costa Rica', 'key': 'CRI'},
                        {'title': 'Mexico', 'key': 'MEX'},
                        {'title': 'Panama', 'key': 'PAN'},
                    ],
                },

                # SOUTH AMERICA
                {
                    'title': 'South America',
                    'key': '_south_america',
                    'children': [
                        {'title': 'Argentina', 'key': 'ARG'},
                        {'title': 'Bolivia', 'key': 'BOL'},
                        {'title': 'Brazil', 'key': 'BRA'},
                        {'title': 'Chile', 'key': 'CHL'},
                        {'title': 'Colombia', 'key': 'COL'},
                        {'title': 'Ecuador', 'key': 'ECU'},
                        {'title': 'Guatemala', 'key': 'GTM'},
                        {'title': 'Honduras', 'key': 'HND'},
                        {'title': 'Nicaragua', 'key': 'NIC'},
                        {'title': 'Peru', 'key': 'PER'},
                        {'title': 'Paraguay', 'key': 'PRY'},
                        {'title': 'El Salvador', 'key': 'SLV'},
                        {'title': 'Uruguay', 'key': 'URY'},

                    ],
                },

                # ASIA
                {
                    'title': 'Asia',
                    'key': '_asia',
                    'children': [
                        {'title': 'Hong Kong', 'key': 'HKG'},
                        {'title': 'Indonesia', 'key': 'IDN'},
                        {'title': 'Japan', 'key': 'JPN'},
                        {'title': 'Malaysia', 'key': 'MYS'},
                        {'title': 'Philippines', 'key': 'PHL'},
                        {'title': 'Singapore', 'key': 'SGP'},
                        {'title': 'Thailand', 'key': 'THA'},
                        {'title': 'Taiwan', 'key': 'TWN'},
                        {'title': 'Vietnam', 'key': 'VNM'},
                    ],
                },

            ]},

    ),
])
af_input = dbc.FormGroup(
    [
        # dbc.Label("Audio feature:", width=2),
        html.Div("Audio feature:", style={'width': '115px'}),
        dbc.Col(
            dcc.Dropdown(
                id='heatmap_audio_feature_dropdown',
                options=[
                    {'label': 'Danceability', 'value': 'danceability'},
                    {'label': 'Valence', 'value': 'valence'},
                    {'label': 'Energy', 'value': 'energy'},
                    {'label': 'Liveness', 'value': 'liveness'},
                    {'label': 'Loudness', 'value': 'loudness'},
                    {'label': 'Speechiness', 'value': 'speechiness'},
                    {'label': 'Acousticness', 'value': 'acousticness'},
                    {'label': 'Instrumentalness', 'value': 'instrumentalness'},
                    {'label': 'Tempo', 'value': 'tempo'},
                    {'label': 'Duration', 'value': 'duration_s'},
                ],
                value=['liveness', 'valence', 'duration_s', ],
                multi=True,
            ),
        )
    ],
    row=True
)

# Layout of row where metric is chosen
dropdown_metric = dbc.FormGroup(
    [
        # dbc.Label("Metric:", width=2),
        html.Div("Metric:", style={'width': '115px'}),
        dbc.Col(
            dcc.Dropdown(
                id='metric_dropdown',
                options=[
                    {'label': 'Mean value', 'value': 'mean'},
                    {'label': 'Median', 'value': 'median'},
                    {'label': 'Standard deviation', 'value': 'std'},
                    {'label': 'Minimum value', 'value': 'amin'},
                    {'label': 'Maximum value', 'value': 'amax'},
                    # {'label': 'Variance', 'value': 'var'},
                ],
                value='mean',
                multi=False,
                clearable=False
            ),
        )
    ],
    row=True
)

# Layout of row where color is chosen
radioitems_color = dbc.FormGroup(
    [
        # dbc.Label("Choose colorscale"),
        html.Div("Colorscale:", style={'width': '115px'}),
        dbc.Col(
            dbc.RadioItems(
                # options=[
                #     {"label": "Option 1", "value": 'af_to_color_dict_hsv'},
                #     {"label": "Option 2", "value": 'af_to_color_dict_lum'},
                # ],
                options=[{'label': key, 'value': key} for key in list(master_dict.keys())],
                value=list(master_dict.keys())[-1],
                id="radioitems_color",
                inline=True,
            ),
        )
    ],
    row=True
)

# Layout of heatmap
layout = dbc.Container(
    [
        html.H2("Audio features over time", id='heatmap_header'),  # style = {'textAlign' : 'center'}
        html.Label(" "),  # Filler
        html.Div([
            dcc.Graph(id='view_heatmap')],
        ),
        # dbc.Form([countries_input, af_input, dropdown_metric, tree_view]),
        dbc.Form([countries_input, af_input, dropdown_metric, radioitems_color]),
    ],
    fluid=True
)


def create_heatmap_figure(mean_vectors, dates, selected_countries, selected_audio_features, metric, af_value_range_dict,
                          af_to_color_dict):
    """ Creates heatmap figure

    :param mean_vectors:
    :param dates:
    :param selected_countries:
    :param selected_audio_features:
    :return:
    """
    selected_countries = np.asarray(selected_countries)
    featuresToTrack = np.asarray([selected_audio_features]).flatten()

    # Create heatmap matrix
    z = create_z_matrix(mean_vectors, dates, selected_countries, featuresToTrack, metric)

    # Create heatmap trace for each feature
    # print(af_to_color_dict)
    traces = []
    for i in range(len(featuresToTrack)):
        tmp_trace, _ = heatmap_trace(z, dates, selected_countries, featuresToTrack, i, af_to_color_dict,
                                     af_value_range_dict,
                                     zrange=af_value_range_dict[featuresToTrack[i]])
        traces.append(tmp_trace)

    # Create figure
    fig = go.Figure(traces)

    tickvals, ticktext = yaxis_ticks(z.shape[0], selected_countries, featuresToTrack)  # Make yaxis ticks
    fig = heatmap_layout(fig, tickvals, ticktext, dates)  # Update layout

    return fig


def create_heatmap_subset_figure(mean_vectors, dates, selected_countries, selected_audio_features, metric,
                                 af_value_range_dict, af_to_color_dict, song_occurences):
    """ Creates heatmap figure where only a subset of the data is colored

    :param mean_vectors:
    :param dates:
    :param selected_countries:
    :param selected_audio_features:
    :return:
    """
    selected_countries = np.asarray([selected_countries]).flatten()
    featuresToTrack = np.asarray([selected_audio_features]).flatten()

    # Create heatmap matrix
    z = create_z_matrix(mean_vectors, dates, selected_countries, featuresToTrack, metric)

    # Create GREYSCALE heatmap traces
    traces = []
    zrange = []  # defines colorbar range. Used for both colored and grescale heatmap
    for i in range(len(featuresToTrack)):
        tmp_trace, tmp_zrange = heatmap_trace(z, dates, selected_countries, featuresToTrack, i, af_to_color_dict,
                                              af_value_range_dict, zrange=af_value_range_dict[featuresToTrack[i]],
                                              greyscale=True)

        zrange.append(tmp_zrange)
        traces.append(tmp_trace)

    # Create COLORED heatmap data
    z_filtered = created_filtered_z_matrix(z, song_occurences, dates, selected_countries, featuresToTrack)
    for i in range(len(featuresToTrack)):  # make trace for each feature
        tmp_trace, tmp_zrange = heatmap_trace(z_filtered, dates, selected_countries, featuresToTrack, i,
                                              af_to_color_dict, af_value_range_dict,
                                              zrange=af_value_range_dict[featuresToTrack[i]])
        traces.append(tmp_trace)

    # Create figure
    fig = go.Figure(traces)
    tickvals, ticktext = yaxis_ticks(z.shape[0], selected_countries, featuresToTrack)  # Make yaxis ticks
    fig = heatmap_layout(fig, tickvals, ticktext, dates)  # Update layout

    return fig


def create_heatmap_yearly_figure(mean_vectors, dates, selected_countries, selected_audio_features):
    """ Creates heatmap figure

    :param mean_vectors:
    :param dates:
    :param selected_countries:
    :param selected_audio_features:
    :return:
    """
    selected_countries = np.asarray(selected_countries)
    selected_countries = [selected_countries[0]]  # Make sure that array only contains one country
    featuresToTrack = np.asarray([selected_audio_features]).flatten()

    weeks = dates.week
    weeks = weeks.unique().sort_values()
    years = dates.year
    years = years.unique().sort_values()

    # Create heatmap matrix
    z = create_z_matrix_yearly(mean_vectors, weeks, years, selected_countries, featuresToTrack)

    # Create heatmap trace for each feature
    traces = []
    for i in range(len(featuresToTrack)):
        tmp_trace, _ = heatmap_trace(z, weeks, selected_countries, featuresToTrack, i, af_to_color_dict,
                                     af_value_range_dict)
        traces.append(tmp_trace)

    # # Create figure
    fig = go.Figure(traces)
    tickvals, ticktext = yaxis_ticks(z.shape[0], years, featuresToTrack)  # Make yaxis ticks
    fig = heatmap_layout(fig, tickvals, ticktext, dates)  # Update layout

    return fig


def create_heatmap_subset_yearly_figure(mean_vectors, dates, selected_countries, selected_audio_features,
                                        song_occurences):
    """ Creates heatmap figure where only a subset of the data is colored

    :param mean_vectors:
    :param dates:
    :param selected_countries:
    :param selected_audio_features:
    :return:
    """

    selected_countries = np.asarray(selected_countries)
    selected_countries = [selected_countries[0]]  # Make sure that array only contains one country
    featuresToTrack = np.asarray([selected_audio_features]).flatten()

    weeks = dates.week
    weeks = weeks.unique().sort_values()
    years = dates.year
    years = years.unique().sort_values()

    # Create heatmap matrix
    z = create_z_matrix_yearly(mean_vectors, weeks, years, selected_countries, featuresToTrack)

    # Create GREYSCALE heatmap traces
    traces = []
    zrange = []  # defines colorbar range. Used for both colored and greyscale heatmap
    for i in range(len(featuresToTrack)):
        tmp_trace, tmp_zrange = heatmap_trace(z, weeks, selected_countries, featuresToTrack, i, af_to_color_dict,
                                              af_value_range_dict, greyscale=True)

        zrange.append(tmp_zrange)
        traces.append(tmp_trace)

    # Create COLORED heatmap data
    z_filtered = created_filtered_z_matrix_yearly(z, song_occurences, weeks, years, featuresToTrack)

    # Make trace for each feature
    for i in range(len(featuresToTrack)):
        tmp_trace, tmp_zrange = heatmap_trace(z_filtered, weeks, selected_countries, featuresToTrack, i,
                                              af_to_color_dict, af_value_range_dict,
                                              zrange[i], z)
        traces.append(tmp_trace)

    # Create figure
    fig = go.Figure(traces)
    tickvals, ticktext = yaxis_ticks(z.shape[0], years, featuresToTrack)  # Make yaxis ticks
    fig = heatmap_layout(fig, tickvals, ticktext, dates)  # Update layout

    return fig


def country_feature_to_yval(country_array, af_array, country=None, feature=None):
    """ Returns the y index of the heatmap corresponding to a given country and feature
    """
    # Calculate index values
    if country in country_array:
        # idx_country = np.where(np.asarray(country_array) == country)[0][0] * len(af_array)
        idx_country = np.where(np.asarray(country_array) == country)[0][0]
    else:
        idx_country = None

    if feature in af_array:
        # idx_af = np.where(np.asarray(af_array) == feature)[0][0]
        idx_af = np.where(np.asarray(af_array) == feature)[0][0] * len(country_array)
    else:
        idx_af = None

    # Decide what to return
    if country and feature:
        return idx_country + idx_af
    elif country:
        return idx_country
    elif feature:
        return idx_af
    else:
        return None


def yval_to_country_feature(y_value, country_array, af_array):
    """ Tells you the country and feature that corresponds to a given y index on the heatmap.

    :param y_value:
    :param country_array:
    :param af_array:
    :return:
    """
    country_idx = y_value % len(country_array)
    feature_idx = y_value // len(country_array)
    selected_country = country_array[country_idx]
    selected_feature = af_array[feature_idx]

    return selected_country, selected_feature


def get_yval_dict(country_array, af_array):
    """ Creates a yval dict that can be used a lookup table. Hopefully adds some efficiency.
    """
    yval_dict = dict()
    for country in country_array:
        yval_dict[country] = dict()
        for feature in af_array:
            yval_dict[country][feature] = country_feature_to_yval(country_array, af_array, country=country,
                                                                  feature=feature)
    return yval_dict


def yaxis_ticks(z_shape, selected_countries, featuresToTrack):
    """ Make tick labels for yaxis

    :param z_shape:
    :param selected_countries:
    :param featuresToTrack:
    :return:
    """

    label_width = 17
    feature_max_len = 11
    tickvals = np.arange(z_shape)
    ticktext = [""] * len(tickvals)
    for i in range(len(ticktext)):
        country, feature = yval_to_country_feature(i, selected_countries, featuresToTrack)

        # Crop feature if it is too long
        feature_max_len = 12
        tmp_feature = dict_col_name_to_label_name[feature]
        if len(tmp_feature) > feature_max_len:
            tmp_feature = tmp_feature[:feature_max_len - 1] + "…"

        # get relative y-val for this country
        y_country = country_feature_to_yval(selected_countries, featuresToTrack, country=country)
        if y_country == len(selected_countries) - 1:  # if this is the 'top' country
            spacing = " " * (label_width - len("{}{} ".format(tmp_feature, country)))
            ticktext[i] = "<b>{}</b>{}{} ".format(tmp_feature, spacing, country)  # .rjust(label_width)
        else:
            ticktext[i] = "{} ".format(country).rjust(label_width)
    return tickvals, ticktext


def heatmap_trace(z, dates_xaxis, selected_countries, featuresToTrack, feature_idx, af_to_color_dict,
                  af_value_range_dict, zrange=None,
                  custom_data=None, greyscale=False, skip_hover=False):
    """ Creates a trace for a audio feature to be plotted in a heatmap

    A trace can have multiple rows, one row for each country.
    """
    mask = np.full_like(z, True).astype(bool)

    row_idx = []
    for country in selected_countries:  # find the rows we want in our trace
        row_idx.append(country_feature_to_yval(selected_countries, featuresToTrack, country=country,
                                               feature=featuresToTrack[feature_idx]))
    mask[row_idx] = False

    tmp_data = z.copy()
    tmp_data[mask] = np.nan

    if zrange is None:
        zrange = (np.nanmin(tmp_data), np.nanmax(tmp_data))
    if custom_data is None:
        custom_data = z

    # Decide if we need to add colorbar or a trace before has done it
    this_color = af_to_color_dict[featuresToTrack[feature_idx]]
    this_range = af_value_range_dict[featuresToTrack[feature_idx]]
    show_color_bar = True
    for i in range(0, feature_idx):  # cycle through features before this one
        if af_to_color_dict[featuresToTrack[i]] == this_color:  # someone else has this colorscale
            if af_value_range_dict[featuresToTrack[i]] == this_range:  # someone else has this color range
                show_color_bar = False  # Someone else has already added it before

    color_bar_index = 0  # Decide where the colorbar should be placed
    cb_title = ''
    if show_color_bar:
        colordict_subset = {key: (af_to_color_dict[key], af_value_range_dict[key]) for key in
                            featuresToTrack}  # Only consider the colors of the included features

        flipped = {}  # Make array of afs with duplicate values
        for key, value in colordict_subset.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                flipped[value].append(key)
        flipped_sorted = sorted(list(flipped.values()), key=len)  # Sort it according to len to decide index
        for i in range(len(flipped_sorted)):
            if featuresToTrack[feature_idx] in flipped_sorted[i]:
                color_bar_index = i

        for af in featuresToTrack:  # Make colorbar multi-line title
            if (af_to_color_dict[af] == this_color) and (af_value_range_dict[af] == this_range):
                cb_title = cb_title + af[0:6].capitalize() + "…" + '<br>'
    colorscale = get_colormap_rgb(af_to_color_dict[featuresToTrack[feature_idx]], 256, greyscale)

    trace = go.Heatmap(
        x=dates_xaxis,
        z=tmp_data,
        colorscale=colorscale,
        hovertemplate="Value: %{customdata:.3f}<br>Interval: %{x} and 7 days forth<br>",
        customdata=custom_data,
        name="",
        colorbar=dict(x=1.020 + 0.11 * color_bar_index,
                      title=cb_title),
        showscale=show_color_bar,
        zmin=zrange[0],
        zmax=zrange[1],
    )

    return trace, zrange


def heatmap_layout(fig, tickvals, ticktext, dates_xaxis):
    """ Defines the layout for the heatmap
    :param fig:
    :param tickvals:
    :param ticktext:
    :return:
    """
    fig.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=8, b=42),
        yaxis=dict(
            tickvals=tickvals,
            ticktext=ticktext,
            fixedrange=True),
        xaxis=dict(
            range=[dates_xaxis[-1], dates_xaxis[0]]
        ),
        font_family="Consolas",
    )
    return fig


def create_z_matrix(mean_vectors, dates, selected_countries, featuresToTrack, metric):
    """ Creates z matrix for heatmap
    :param mean_vectors:
    :param dates:
    :param selected_countries:
    :param featuresToTrack:
    :return:
    """
    # Initialize heatmap matrix
    z = np.empty((len(dates), len(selected_countries) * featuresToTrack.shape[0])) * np.nan

    # Initialize yval dict
    yval_dict = get_yval_dict(selected_countries, featuresToTrack)

    # Iterate over dates
    # for date in dates:
    #     x = np.where(dates == date)[0]

    for i in range(len(selected_countries)):
        songs_cur_country = get_subset(mean_vectors, {"region": [selected_countries[i]]})

        # Get dates for current country
        # dates_cur_country = songs_cur_country.date
        dates_cur_country = [date.strftime('"%Y-%m-%d"') for date in songs_cur_country.date]

        # Get all dates in same format
        all_dates = [date.strftime('"%Y-%m-%d"') for date in dates]
        # all_dates = [datetime.datetime.strftime(date, '"%Y-%m-%d"') for date in dates]

        # Create mask, indicating whether data exists for different weeks for current country
        week_mask = np.zeros(len(dates), dtype=bool)
        for x in range(len(all_dates) - 1, -1, -1):
            if all_dates[x] in dates_cur_country:
                week_mask[x] = True

        n_weeks_total = len(all_dates)
        n_weeks_skipped = 0  # keep track of how many weeks have been skipped, used to not over-index
        for x in range(len(dates)):
            if week_mask[x] == True:  # if data for given week exists for given country,
                dataset = songs_cur_country.iloc[-1 - (x - n_weeks_skipped)]
                for feature in featuresToTrack:
                    y = yval_dict[selected_countries[i]][feature]
                    z[x, y] = dataset[feature][metric]
            else:
                n_weeks_skipped = n_weeks_skipped + 1

        # for country in selected_countries:
        #     dataset = get_subset(songs_cur_date, {"region": [country]})

    # # iterates through each combination of selected_countries and dates
    # for country, date in itertools.product(selected_countries, dates):
    #     # Finds the heatmap x index for the current date
    #     x = np.where(dates == date)[0]
    #
    #     # Finds the audio feature dictionary for the selected region and date
    #     # dataset = mean_vectors.loc[(mean_vectors['region'] == country) & ((mean_vectors['date'] == date))]
    #     dataset = get_subset(mean_vectors, {"region": [country], 'date': [date]})
    #
    #     # Insert the data point in the z map
    #     if len(dataset) > 0:
    #         for feature in featuresToTrack:
    #             y = yval_dict[country][feature]
    #             z[x, y] = dataset[feature][metric]

    # Flip it around so the heatmap can understand it
    return z.T


def created_filtered_z_matrix(z, song_occurences, dates, selected_countries, featuresToTrack):
    """ Make filtered version of z matrix, where there is only values in cells that have a song occuruence. The rest
    of the values are np.nan
    :param z:
    :param song_occurences:
    :param dates:
    :param selected_countries:
    :param featuresToTrack:
    :return:
    """
    # Initialize yval dict
    yval_dict = get_yval_dict(selected_countries, featuresToTrack)
    # Initialize grey mask
    grey_mask = np.full_like(z.T, True).astype(bool)

    for row, occurence in song_occurences.iterrows():
        # Finds the heatmap x index for the current date
        target_date = occurence['date']
        x = np.where(dates == target_date)

        # Finds the heatmap y index for the current country and feature
        target_region = occurence['region']

        # Insert the data point in the grey_mask
        for feature in featuresToTrack:
            y = yval_dict[target_region][feature]
            grey_mask[x, y] = False

    # Flip it around so the heatmap can understand it
    grey_mask = grey_mask.T
    # Use grey mask to set all irrelevant values to np.nan
    z_filtered = z.copy()
    z_filtered[grey_mask] = np.nan

    return z_filtered


def add_bounding_box_to_heatmap(fig, date, row_min, row_max):
    fig.add_shape(type="rect",
                  x0=(date - datetime.timedelta(days=3, hours=12)), y0=row_min - 0.485,
                  x1=(date + datetime.timedelta(days=3, hours=12)), y1=row_max + 0.485,
                  line=dict(
                      color="Black",
                      width=2,
                  ),
                  fillcolor="rgba(255, 0, 0, 0)",
                  opacity=1
                  )


def add_white_space_between_audio_features(fig, dates, n_countries, n_audio_features):
    for i in range(1, n_audio_features):
        fig.add_shape(type="line",
                      x0=(dates[0] + datetime.timedelta(days=3, hours=12)), y0=i * n_countries - 0.5,
                      x1=(dates[-1] - datetime.timedelta(days=3, hours=12)), y1=i * n_countries - 0.5,
                      line=dict(
                          color="White",
                          width=4,
                      ),
                      )


def add_chart_position(fig, song_occurences, selected_regions, selected_audio_features, dates_xaxis):
    for region in selected_regions:
        # Get song occurences for region
        regional_occurences = get_subset(song_occurences, {'region': [region]})

        dates = regional_occurences.date
        chart_positions = regional_occurences.Position

        region_no = selected_regions.index(region)
        for af in selected_audio_features:
            af_no = selected_audio_features.index(af)
            max_y_val = region_no + 0.5 + len(selected_regions) * af_no
            min_y_Val = max_y_val - 1
            dy_dpos = 1 / 200 * (max_y_val - min_y_Val)
            trace = go.Scatter(x=dates,
                               y=max_y_val - (chart_positions - 1) * dy_dpos,
                               mode='markers',
                               customdata=chart_positions,
                               marker_color="black",
                               marker_size=2,
                               showlegend=False,
                               hoverinfo="skip",
                               )
            fig.add_trace(trace)
    fig.update_yaxes(range=[-0.5, len(selected_audio_features) * len(selected_regions) - 0.5])
    fig.update_xaxes(range=[dates_xaxis[-1], dates_xaxis[0]])
