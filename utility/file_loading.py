from datetime import datetime
import pandas as pd
import os
import glob


def load_files(data_path, regions=None, prefix=None, debug_log=False):
    """
    :param data_path: Path to folder containing files
    :param regions: List of region abbreviation in ISO3 format
    :param prefix: Part of the filename that is before the unique region identifiers
    :param debug_log: Decides if the function should print the progress to console
    :return: pandas dataframe with the requested data
    """
    if prefix is None:
        prefix_ = 'af_weekly_'
    else:
        prefix_ = prefix

    if regions is not None:
        af_filenames = regions_to_filenames(data_path, regions, prefix_)
    else:  # load all regions
        glob_string = glob.glob(os.path.join(data_path, prefix_+'*'))
        af_filenames = [os.path.basename(file) for file in glob_string]

    if debug_log is True:
        print("Loading data to memory")
        print("Total files: {}".format(len(af_filenames)))
        print("Files loaded: ", end='')
        file_counter = 1

    li = []
    dateparser = lambda x: datetime.strptime(x, '%d-%m-%Y')
    for filename in af_filenames:
        df = pd.read_csv(os.path.join(data_path,filename), index_col=None, header=0, parse_dates=['date'], date_parser=dateparser)
        li.append(df)

        if debug_log is True:
            print("{} ".format(file_counter), end='')
            file_counter = file_counter + 1
    if debug_log is True:
        print()
        print("Load complete")

    data = pd.concat(li, axis=0, ignore_index=True)
    return data


def regions_to_filenames(data_path, regions, prefix):
    """
    :param data_path: Path to folder containing files
    :param regions: List of region abbreviation in ISO3 format
    :param prefix: Part of the filename that is before the unique region identifiers
    :return: list of filenames
    """
    filenames = []
    for r in regions:
        filenames.append(str(region_to_filename(data_path, r, prefix)))
    return filenames


def region_to_filename(data_path, region, prefix):
    """
    :param data_path: Path to folder containing file
    :param region: String with region abbreviation in ISO3 format
    :param prefix: Part of the filename that is before the unique region identifier
    :return: filename for the desired region
    """
    glob_string = glob.glob(os.path.join(data_path, prefix+region+'*'))
    af_filenames = [os.path.basename(file) for file in glob_string]  # handled as an list in case of multiple hits
    return af_filenames[0]


