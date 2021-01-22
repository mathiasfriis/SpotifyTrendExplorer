""" Matplotlib to dash colormap conversion
https://plotly.com/python/v3/matplotlib-colorscales/
"""
import matplotlib
from matplotlib import cm, colors
import numpy as np
import plotly.express as px
import colorlover


def grayscale_cmap(cmap):
    """Return a grayscale version of the given colormap"""
    # cmap = cm.get_cmap(cmap)
    map_colors = cmap(np.arange(cmap.N))

    # convert RGBA to perceived grayscale luminance
    # cf. http://alienryderflex.com/hsp.html
    RGB_weight = [0.299, 0.587, 0.114]
    luminance = np.sqrt(np.dot(map_colors[:, :3] ** 2, RGB_weight))
    map_colors[:, :3] = luminance[:, np.newaxis]

    return colors.LinearSegmentedColormap.from_list(cmap.name + "_gray", map_colors, cmap.N)


def matplotlib_to_rgb(cmap, pl_entries):
    h = 1.0 / (pl_entries - 1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(np.array(cmap(k * h)[:3]) * 255)
        pl_colorscale.append('rgb' + str((C[0], C[1], C[2])))

    return pl_colorscale


def get_colormap_rgb(name, n_bins=100, grey=False):
    if name == 'hsv':
        cmap_matplotlib = get_continuous_cmap(px.colors.cyclical.HSV, n_bins=256)
    elif name == 'hsv2':
        tmp_list = list()
        for i in range(2):
            tmp_list = tmp_list + px.colors.cyclical.HSV
        cmap_matplotlib = get_continuous_cmap(tmp_list, n_bins=256)
    elif name == 'hsv3':
        tmp_list = list()
        for i in range(5):
            tmp_list = tmp_list + px.colors.cyclical.HSV
        cmap_matplotlib = get_continuous_cmap(tmp_list, n_bins=256)
    elif name == 'phase':
        cmap_matplotlib = get_continuous_cmap(px.colors.cyclical.Phase, n_bins=256, rgb=True)
    elif name == 'phase2':
        tmp_list = list()
        for i in range(2):
            tmp_list = tmp_list + px.colors.cyclical.Phase
        cmap_matplotlib = get_continuous_cmap(tmp_list, n_bins=256, rgb=True)
    elif name == 'phase3':
        tmp_list = list()
        for i in range(5):
            tmp_list = tmp_list + px.colors.cyclical.Phase
        cmap_matplotlib = get_continuous_cmap(tmp_list, n_bins=256, rgb=True)
    elif name == 'turbo2':
        cmap_matplotlib = matplotlib.cm.get_cmap('turbo')
        # Also needs something to be done in the end of the function (see further down)
    elif type(name) == tuple:
        cmap_matplotlib = get_continuous_cmap(name, n_bins=256, rgb=True)

    else:
        cmap_matplotlib = matplotlib.cm.get_cmap(name)

    if grey:  # make greyscale version
        cmap_matplotlib = grayscale_cmap(cmap_matplotlib)

    cmap_rgb = matplotlib_to_rgb(cmap_matplotlib, n_bins)

    if name == 'turbo2':
        cmap_rgb = cmap_rgb + cmap_rgb[::-1]

    return cmap_rgb


def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#")  # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v / 256 for v in value]


def get_continuous_cmap(hex_list, float_list=None, n_bins=256, rgb=False):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list.

        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        rgb_list: bool indiciating that input is already in rgb

        Returns
        ----------
        colour map'''
    if not rgb:
        rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    else:
        hex_list = colorlover.to_numeric(hex_list)
        rgb_list = [rgb_to_dec(i) for i in hex_list]

    if float_list:
        pass
    else:
        float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = colors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=n_bins)
    return cmp
