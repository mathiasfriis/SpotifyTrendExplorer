import pandas as pd


def filter_by_region(data, region):
    """ Efficient method to filter data by region

    :param data: Pandas dataframe
    :param region: ISO3 string with the desired region
    :return: data for the desired region
    """
    query = "region == @region"
    filtered_data = data.query(query)
    return filtered_data

def filter_by_position(data, position):
    """ Efficient method to filter data by region

    :param data: Pandas dataframe
    :param position: the lowest position you want
    :return: data for the desired region
    """
    query = "Position <= @position"
    filtered_data = data.query(query)
    return filtered_data


def filter_by_region_and_date(data,region,date):
    """ Efficient method to filter data by region and data

    :param data: Pandas dataframe
    :param region: ISO3 string with the desired region
    :param date: datetime64 value of the desired date
    :return: data for the desired region and date
    """
    filtered_data = filter_by_region(data,region)
    filtered_data = filtered_data.query("date == @date")
    return filtered_data

def get_subset(data, filter_dict):
    """
    Get a subset of the provided data frame
    :param data: pandas data frame
    :param filter_dict: Dictionary, where key indicates a feature we want to sort by, and the value indicates the desired values.
    :return: pandas data frame
    """
    data_filtered = data
    for attr in filter_dict.keys():
        include_vals = filter_dict[attr]
        indice_to_include = data_filtered[attr].isin(include_vals)
        data_filtered = data_filtered[indice_to_include]
        # print(data_filtered)
    return data_filtered