from unittest.mock import MagicMock
from mlmonitoring.client import Client
import pandas as pd


def generate_dataframe():
    table = [
        [i, 0] for i in range(50)
    ] + [
        [i+50, 1] for i in range(50) 
    ]
    dataframe = pd.DataFrame(
        table,
        columns=['key', 'value']
    )
    return dataframe


def client_insert_side_effect(route, json=None):
    return route, json


def test_client_insert(monkeypatch):
    mock_session = MagicMock(side_effect=client_insert_side_effect)
    monkeypatch.setattr('requests.Session.post', mock_session)

    client = Client()
    dataframe = generate_dataframe()

    request = client.insert(
        dataframe,
        'project_name',
        'insert_table'
    )

    mock_session.assert_called_once_with(
        'http://127.0.0.1:8000/insert',
        json=request[1]
    )


def test_client_view(monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr('requests.Session.get', mock_session)

    client = Client()

    request = client.view(
        'project_name',
        'view_table'
    )

    mock_session.assert_called_once_with(
        'http://127.0.0.1:8000/view/project_name_view_table'
    )


def test_client_filter(monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr('requests.Session.get', mock_session)

    client = Client()

    request = client.filter(
        'project_name',
        'filter_table',
        'value__gt__0.5'
    )

    mock_session.assert_called_once_with(
        'http://127.0.0.1:8000/filter/project_name_filter_table/value__gt__0.5'
    )
    
