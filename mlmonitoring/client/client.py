import json
import requests
import pandas as pd
from typing import Union


DataFrame = Union[pd.DataFrame, pd.Series]


class Client:
    """Client class to be used in order
    to make requests to the server side
    """

    def __init__(self):
        self._api_url = 'http://127.0.0.1:8000'

    def set_connection(self, api_url: str):
        """Define the connection to the server.

        Args:
            api_url (str): The API URL.
        """

        self._api_url = api_url

    def insert(self, dataframe: DataFrame, project_name: str, table_name: str):
        """Inserts a Pandas DataFrame/Series to the project database table.

        Args:
            dataframe (DataFrame): A DataFrame/Series to insert.
            project_name (str): The name of the project.
            table_name (str): The name of the table.

        Returns:
            requests.Response: The response of the request.
        """

        data = {
            "table_name": '{}_{}'.format(project_name, table_name),
            "dataframe": json.loads(dataframe.to_json(orient='table'))
        }

        with requests.Session() as session:
            adapter = requests.adapters.HTTPAdapter()
            session.mount(self._api_url, adapter)

            route = '{}/insert'.format(self._api_url)
            req = session.post(route, json=data)
            return req

    def view(self, project_name: str, table_name: str):
        """Returns the table as a DataFrame.

        Args:
            project_name (str): The name of the project.
            table_name (str): The name of the table.

        Returns:
            requests.Response: The response of the request.
        """

        with requests.Session() as session:
            adapter = requests.adapters.HTTPAdapter()
            session.mount(self._api_url, adapter)

            route = '{}/view/{}_{}'.format(
                self._api_url,
                project_name,
                table_name
            )
            req = session.get(route)
            return req

    def filter(self, project_name: str, table_name: str, query_string: str):
        with requests.Session() as session:
            adapter = requests.adapters.HTTPAdapter()
            session.mount(self._api_url, adapter)

            route = '{}/filter/{}_{}/{}'.format(
                self._api_url,
                project_name,
                table_name,
                query_string
            )
            req = session.get(route)
            return req
