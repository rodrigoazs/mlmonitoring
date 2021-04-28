from click.testing import CliRunner
from unittest import mock
import os
import pytest


@mock.patch.dict(os.environ, {
    "MLMONITOR_DATABASE_URI": "sqlite:///:memory:"
})
def test_cli():
    with mock.patch("uvicorn.run") as run_server_mock:
        from mlmonitoring.server.main import cli
        runner = CliRunner()
        result = runner.invoke(cli, [
            '--host',
            '0.0.0.0',
            '--port',
            '8000'
        ])
        run_server_mock.assert_called_once()
        assert result.exit_code == 0
        assert result.output == 'Initializing MLmonitoring server\n'
