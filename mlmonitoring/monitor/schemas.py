from typing import Callable, List, Optional, Union
from mlmonitoring.client import Client
from mlmonitoring.monitor.checks import Check


CheckList = Optional[
    Union[Check, List[Check]]
]


class Monitoring:
    """A monitoring policy.

    Arguments:
        method {Callable} -- A monitoring method.

    Keyword Arguments:
        low_risk {CheckList} -- List of checks in order to
        warning low risk cases. (default: {None})
        high_risk {CheckList} -- List of checks in order to
        warning high risk cases. (default: {None})
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
        return self._table_name

    def __call__(self):
        results = self._method(*self._param_args, **self._param_kwargs)

        lr = []
        for risk in self._low_risk:
            warning, cases = risk(results)
            if warning:
                lr.append((risk.name, cases))

        hr = []
        for risk in self._high_risk:
            warning, cases = risk(results)
            if warning:
                hr.append((risk.name, cases))

        return {
            'table_name': self._table_name,
            'results': results,
            'low_risk': lr,
            'high_risk': hr,
        }


class MLmonitoring:
    def __init__(self):
        self._monitors = []
        self._client = Client()
        self._project = ''
        
    def set_connection(self, api_url):
        self._client.set_connection(api_url)
        return self
    
    def set_project(self, project_name):
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
        all_results = []
        for monitor in self._monitors:
            results = monitor()
            all_results.append(results)
            self._client.insert(
                results,
                self._project,
                monitor.get_table_name()
            )
        return all_results
