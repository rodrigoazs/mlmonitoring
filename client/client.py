import json
import requests


class Client:
    def __init__(self):
        self._api_url = 'http://127.0.0.1:8000'

    def set_connection(self, api_url):
        self._api_url = api_url

    def insert(self, dataframe, project_name, table_name):
        data = {
            "table_name": '{}_{}'.format(project_name, table_name),
            "dataframe": json.loads(dataframe.to_json(orient='table'))
        }

        with requests.Session() as session:
            adapter = requests.adapters.HTTPAdapter()
            session.mount(self._api_url, adapter)

            route = '{}/insert'.format(self._api_url)
            req = session.post(route, json=data)
            return {"status_code ": req.status_code}, {"status_response ": req.text}

    def view(self, project_name, table_name):
        with requests.Session() as session:
            adapter = requests.adapters.HTTPAdapter()
            session.mount(self._api_url, adapter)

            route = '{}/view/{}_{}'.format(self._api_url, project_name, table_name)

            req = session.get(route)

            return req.text