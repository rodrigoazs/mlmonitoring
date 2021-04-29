from unittest import mock
import os
import pytest
import json
import pandas as pd
from mlmonitoring.server.schemas import InsertModel
from sqlalchemy.exc import OperationalError


def generate_model(table_name):
    table = [
        [i, 0] for i in range(50)
    ] + [
        [i+50, 1] for i in range(50) 
    ]
    dataframe = json.loads(pd.DataFrame(
        table,
        columns=['key', 'value']
    ).to_json(orient='table'))

    model = InsertModel(
        table_name=table_name,
        dataframe=dataframe
    )
    return model


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_insert_table():
    from mlmonitoring.server.store import insert_table

    model = generate_model('test_insert')   

    result = insert_table(model)
    assert result == None


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_view_table_inserted_table():
    from mlmonitoring.server.store import insert_table, view_table

    model = generate_model('test_view')
    insert_table(model)

    result = view_table('test_view')
    assert type(result) == str


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_view_inexistent_table_raises_operational_error():
    from mlmonitoring.server.store import view_table

    with pytest.raises(OperationalError):
        result = view_table('teste_view_inexistent')


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_filter_table():
    from mlmonitoring.server.store import insert_table, filter_table

    model = generate_model('teste_filter')
    insert_table(model)

    result = filter_table(
        'teste_filter',
        'value__gt__0.5'
    )

    assert len(json.loads(result)) == 50
