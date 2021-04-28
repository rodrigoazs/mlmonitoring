from unittest import mock
import os
import pytest
import json
import pandas as pd
from mlmonitoring.server.schemas import InsertModel
from sqlalchemy.exc import OperationalError


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_insert_table():
    from mlmonitoring.server.store import insert_table

    table_name = 'table_name'
    dataframe = json.loads(pd.DataFrame(
        [[1,2], [3,4]],
        columns=['key', 'value']
    ).to_json(orient='table'))

    model = InsertModel(
        table_name=table_name,
        dataframe=dataframe
    )

    result = insert_table(model)
    assert result == None


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_view_table_inserted_table():
    from mlmonitoring.server.store import insert_table, view_table

    table_name = 'table_name'
    dataframe = json.loads(pd.DataFrame(
        [[1,2], [3,4]],
        columns=['key', 'value']
    ).to_json(orient='table'))

    model = InsertModel(
        table_name=table_name,
        dataframe=dataframe
    )

    insert_table(model)

    result = view_table('table_name')
    assert type(result) == str


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_view_inexistent_table_raises_operational_error():
    from mlmonitoring.server.store import view_table

    with pytest.raises(OperationalError):
        result = view_table('fake_table')
