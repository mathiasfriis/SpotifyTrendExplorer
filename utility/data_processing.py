import numpy as np

import pandas as pd
import itertools

from scipy.stats import zscore


def create_mean_vectors(data):

    metrics_to_include = [np.mean, np.std, np.min, np.max, np.median, np.var];

    mean_vectors = data.groupby(['date', 'region','year','week']).agg(
        {'danceability': metrics_to_include,
         'valence': metrics_to_include,
         'energy': metrics_to_include,
         'loudness': metrics_to_include,
         'speechiness': metrics_to_include,
         'acousticness': metrics_to_include,
         'instrumentalness': metrics_to_include,
         'liveness': metrics_to_include,
         'tempo': metrics_to_include,
         'duration_ms': metrics_to_include,
         'duration_s': metrics_to_include,
         }).reset_index()
    return mean_vectors

def create_unique_dates(data):
    dates = data['date']
    dates = dates.unique()
    dates = pd.to_datetime(dates, dayfirst=True)
    return dates



def create_heatmap_matrix_given_songs_and_audio_features(songs, audioFeatures):

    # Given subset of data, iterate to create matrix

    z = np.empty((len(songs), len(audioFeatures),)) * np.nan
    # z = np.empty((len(regions), len(dates),)) * np.nan

    for index, s in songs.iterrows():
        i = np.where(songs["Track Name"] == s["Track Name"])
        i = index
        for j in range(0,len(audioFeatures)):
            af = audioFeatures[j]
            val = s[af]
            z[i,j] = val

    return z


# Get ranges for the given columns in a data set using provided quantiles
def create_range_dictionary(data, column_names, lower_quantile, upper_quantile):
    af_value_range_dict = {}
    for cn in column_names:
        af_value_range_dict[cn] = [data[cn].quantile(lower_quantile), data[cn].quantile(upper_quantile),]
    return af_value_range_dict

# Get ranges for the given columns in a data set using z-score outlier detection
def create_range_dictionary(data, column_names):
    af_value_range_dict = {}
    for cn in column_names:
        # Extract column values
        col_vals = data[cn]
        # remove extreme outliers from column values
        col_vals = col_vals[(np.abs(zscore(col_vals)) < 3)]
        # Get min and max
        af_value_range_dict[cn] = [col_vals.min(), col_vals.max(),]
    return af_value_range_dict

