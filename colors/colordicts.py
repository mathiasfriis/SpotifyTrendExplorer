from colors.legacy_colors import *

# Dynamically create ranges for the different parameters
# af_value_range_dict =  create_range_dictionary(data, available_audio_features)
af_value_range_dict = {
    'danceability': (0, 1),
    'valence': (0, 1),
    'energy': (0, 1),
    'liveness': (0, 1),
    'loudness': (-20, 2),
    'speechiness': (0, 1),
    'acousticness': (0, 1),
    'instrumentalness': (0, 1),
    'tempo': (50, 220),
    'duration_ms': (90000, 450000),
    'duration_s': (90, 450),
}

# Map af to a colour map  # https://plotly.com/python/builtin-colorscales/


af_to_color_dict_lum = {
    'danceability': 'viridis',
    'valence': 'viridis',
    'energy': 'viridis',
    'liveness': 'viridis',
    'loudness': 'parula',
    'speechiness': 'viridis',
    'acousticness': 'viridis',
    'instrumentalness': 'viridis',
    'tempo': 'plasma',
    'duration_ms': 'cividis',
    'duration_s': 'cividis',
}

af_to_color_dict_turbo = {
    'danceability': 'turbo',
    'valence': 'turbo',
    'energy': 'turbo',
    'liveness': 'turbo',
    'loudness': 'turbo',
    'speechiness': 'turbo',
    'acousticness': 'turbo',
    'instrumentalness': 'turbo',
    'tempo': 'turbo',
    'duration_ms': 'turbo',
    'duration_s': 'turbo',
}

af_to_color_dict_turbo2 = {
    'danceability': 'turbo2',
    'valence': 'turbo2',
    'energy': 'turbo2',
    'liveness': 'turbo2',
    'loudness': 'turbo2',
    'speechiness': 'turbo2',
    'acousticness': 'turbo2',
    'instrumentalness': 'turbo2',
    'tempo': 'turbo2',
    'duration_ms': 'turbo2',
    'duration_s': 'turbo2',
}

af_to_color_dict_hsv = {
    'danceability': 'hsv',
    'valence': 'hsv',
    'energy': 'hsv',
    'liveness': 'hsv',
    'loudness': 'hsv',
    'speechiness': 'hsv',
    'acousticness': 'hsv',
    'instrumentalness': 'hsv',
    'tempo': 'hsv',
    'duration_ms': 'hsv',
    'duration_s': 'hsv',
}

af_to_color_dict_hsv2 = {
    'danceability': 'hsv2',
    'valence': 'hsv2',
    'energy': 'hsv2',
    'liveness': 'hsv2',
    'loudness': 'hsv2',
    'speechiness': 'hsv2',
    'acousticness': 'hsv2',
    'instrumentalness': 'hsv2',
    'tempo': 'hsv2',
    'duration_ms': 'hsv2',
    'duration_s': 'hsv2',
}

af_to_color_dict_hsv3 = {
    'danceability': 'hsv3',
    'valence': 'hsv3',
    'energy': 'hsv3',
    'liveness': 'hsv3',
    'loudness': 'hsv3',
    'speechiness': 'hsv3',
    'acousticness': 'hsv3',
    'instrumentalness': 'hsv3',
    'tempo': 'hsv3',
    'duration_ms': 'hsv3',
    'duration_s': 'hsv3',
}

af_to_color_dict_phase = {
    'danceability': 'phase',
    'valence': 'phase',
    'energy': 'phase',
    'liveness': 'phase',
    'loudness': 'phase',
    'speechiness': 'phase',
    'acousticness': 'phase',
    'instrumentalness': 'phase',
    'tempo': 'phase',
    'duration_ms': 'phase',
    'duration_s': 'phase',
}

af_to_color_dict_phase2 = {
    'danceability': 'phase2',
    'valence': 'phase2',
    'energy': 'phase2',
    'liveness': 'phase2',
    'loudness': 'phase2',
    'speechiness': 'phase2',
    'acousticness': 'phase2',
    'instrumentalness': 'phase2',
    'tempo': 'phase2',
    'duration_ms': 'phase2',
    'duration_s': 'phase2',
}

af_to_color_dict_phase3 = {
    'danceability': 'phase3',
    'valence': 'phase3',
    'energy': 'phase3',
    'liveness': 'phase3',
    'loudness': 'phase3',
    'speechiness': 'phase3',
    'acousticness': 'phase3',
    'instrumentalness': 'phase3',
    'tempo': 'phase3',
    'duration_ms': 'phase3',
    'duration_s': 'phase3',
}

master_dict = {
    'v.1 Categorical colors': af_colordict_cb_set3,
    'v.2 Perceptually Uniform': af_to_color_dict_lum,
    'v.3a Turbo': af_to_color_dict_turbo,
    'v.3b Cyclic HSV x2': af_to_color_dict_hsv2,
    # 'Turbo x2': af_to_color_dict_turbo2,
    # 'Cyclic HSV': af_to_color_dict_hsv,
    # 'Cyclic HSV x5': af_to_color_dict_hsv3,
    # 'Phase': af_to_color_dict_phase,
    # 'Phase x2': af_to_color_dict_phase2,
    # 'Phase x5': af_to_color_dict_phase3,
}
