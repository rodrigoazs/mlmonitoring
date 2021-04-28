from fastapi.testclient import TestClient
from unittest import mock
import os


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_view_inexistent_dataframe_in_database():
    from mlmonitoring.server.main import app
    client = TestClient(app)
    response = client.get("/view/inexistent_table")
    assert response.status_code == 500
