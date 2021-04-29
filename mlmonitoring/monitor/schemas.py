from typing import Callable, List, Optional, Union
from mlmonitoring.client import Client
from mlmonitoring.monitor.checks import Check
import pandas as pd
import json
import logging


_logger = logging.getLogger(__name__)


CheckList = Optional[
    Union[Check, List[Check]]
]


class Monitoring:
    """A monitoring policy containing a method and its checks.

    Args:
        table_name (str): The name of the table to be created/inserted.
        method (Callable): A monitoring method to apply.
        param_args (tuple, optional): Arguments of the method. Defaults to ().
        param_kwargs (dict, optional): Arguments of the method. Defaults to {}.
        low_risk (CheckList, optional): Low risk checks to be
        applied. Defaults to None.
        high_risk (CheckList, optional): High risk checks to be
        applied. Defaults to None.
    """
    
    def __init__(
        self,
        table_name: str,
        method: Callable,
        param_args=(),
        param_kwargs={},
        low_risk: CheckList = None,
        high_risk: CheckList = None
    ) -> None:
        self._table_name = table_name
        self._method = method
        self._param_args = param_args
        self._param_kwargs = param_kwargs
        self._low_risk = low_risk if isinstance(low_risk, list) \
            else [] if low_risk is None \
            else [low_risk]
        self._high_risk = high_risk if isinstance(high_risk, list) \
            else [] if high_risk is None \
            else [high_risk]
        
    def get_table_name(self):
        """Return the table name of the monitoring method.

        Returns:
            str: The table name.
        """

        return self._table_name

    def __call__(self):
        """Call function for the monitoring method.

        Returns:
            dict: A dictionary with information about the applied
            method.
        """

        results = self._method(*self._param_args, **self._param_kwargs)

        # low risk checks
        low_risk_checks = []
        for risk in self._low_risk:
            warning, cases = risk(results)
            if warning:
                low_risk_checks.append((risk.name, cases))

        # high_risk checks
        high_risk_checks = []
        for risk in self._high_risk:
            warning, cases = risk(results)
            if warning:
                high_risk_checks.append((risk.name, cases))

        return {
            'table_name': self._table_name,
            'results': results,
            'low_risk': low_risk_checks,
            'high_risk': high_risk_checks,
        }


class MLmonitoring:
    """Monitoring class to append monitoring methods
    in sequence.
    """
    
    def __init__(self):
        self._monitors = []
        self._client = Client()
        self._project = ''
        
    def set_connection(self, api_url):
        """Sets the server connection.

        Args:
            api_url (str): Endpoint for the server.
        """

        self._client.set_connection(api_url)
        return self
    
    def set_project(self, project_name):
        """Sets the project name.

        Args:
            project_name (str): The project name.
        """

        self._project = project_name
        return self

    def append(
        self,
        table_name: str,
        method: Callable,
        param_args=(),
        param_kwargs={},
        low_risk: CheckList = None,
        high_risk: CheckList = None
    ) -> None:
        """Append a monitoring method.

        Args:
            table_name (str): The name of the table to be created/inserted.
            method (Callable): A monitoring method to apply.
            param_args (tuple, optional): Arguments of the method. Defaults to ().
            param_kwargs (dict, optional): Arguments of the method. Defaults to {}.
            low_risk (CheckList, optional): Low risk checks to be
            applied. Defaults to None.
            high_risk (CheckList, optional): High risk checks to be
            applied. Defaults to None.
        """

        self._monitors.append(Monitoring(
            table_name,
            method,
            param_args,
            param_kwargs,
            low_risk,
            high_risk))
        return self

    def run(
        self
    ) -> None:
        """Run the monitoring system.

        Returns:
            dict: A dictionary with the results of each
            monitoring method.
        """

        all_results = []
        for monitor in self._monitors:
            results = monitor()
            all_results.append(results)
            self._client.insert(
                results['results'],
                self._project,
                monitor.get_table_name()
            )
            _logger.info('Inserted data to {}_{}'.format(
                self._project,
                monitor.get_table_name()
            ))
        return all_results

    def view(
        self,
        table_name: str
    ) -> pd.DataFrame:
        req = self._client.view(
            self._project,
            table_name,
        )
        return pd.read_json(json.loads(req.text), orient='records')
  
    def filter(
        self,
        table_name: str,
        **kwargs
    ) -> pd.DataFrame:
        query_string = []
        for key, value in kwargs.items():
            query_string.append(
                '{}__{}'.format(key, value)
            )
        query_string = '&'.join(query_string)

        req = self._client.filter(
            self._project,
            table_name,
            query_string
        )

        return pd.read_json(json.loads(req.text), orient='records')
