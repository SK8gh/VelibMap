import matplotlib.pyplot as plt
import pandas as pd
import requests
import logging

import configuration as conf


class QueryAPI:
    def __init__(self):
        self._station_info_url = conf.station_info_url
        self._station_status_url = conf.station_status_url

    @staticmethod
    def _get_info(url):
        try:
            response = requests.get(url).json()
        except Exception as e:
            logging.error(f"Could not retrieve station information")
            raise e

        data = response['data']['stations']
        return data

    def _get_locations(self):
        """
        Unpacking locations from the data retrieve using the private method _get_station_info
        :return:
        """
        data = QueryAPI._get_info(self._station_info_url)

        # Building a dataframe containing the locations of the Vélib stations
        locations_df = pd.DataFrame(columns=['NAME', 'STATION_ID', 'LAT', 'LON'])

        # Keys of interest
        keys = ['name', 'station_id', 'lat', 'lon']

        for d in data:
            new_row = [d.get(k) for k in keys]
            locations_df.loc[len(locations_df)] = new_row

        # Locations sorted by ID
        result = locations_df.sort_values(by='STATION_ID')

        if not result.empty:
            logging.info(f"Retrieved locations of {len(result)} Vélib stations successfully")
            return result

        logging.error(f"Couldn't retrieve locations correctly")

    def _get_stations_status(self):
        station_status = QueryAPI._get_info(self._station_status_url)

        # Building a dataframe containing the locations of the Vélib stations
        columns = ['STATION_ID', 'NUM_DOCKS_AVAILABLE', 'NUM_MECHANICAL', 'NUM_E_BIKES']
        station_status_df = pd.DataFrame(columns=columns)

        # Keys of interest
        keys = ['station_id', 'num_docks_available']

        for d in station_status:
            new_row = [d.get(k) for k in keys]

            num_bikes_by_type = d['num_bikes_available_types']

            for elt, key in zip(num_bikes_by_type, ['mechanical', 'ebike']):
                new_row.append(elt[key])

            station_status_df.loc[len(station_status_df)] = new_row

        # Locations sorted by name
        result = station_status_df.sort_values(by='STATION_ID')

        if not result.empty:
            logging.info(f"Retrieved stations status with length {len(result)} successfully")
            return result

        logging.error(f"Couldn't retrieve status correctly")

    def get_data(self):
        """
        'Main' method to call to retrieve data about the stations themselves and their respective status information
        :return:
        """
        # Stations status
        stations_status_df = self._get_stations_status()

        # Locations
        locations_df = self._get_locations()

        # Merging both dataframes to get the most exhaustive data we can
        data = pd.merge(stations_status_df, locations_df, on='STATION_ID')

        # Ordering by station name
        data.sort_values(by='NAME', inplace=True)

        return data
