# MLmonitoring

MLmonitoring is a platform for monitoring machine learning models in production in order to track and understand models' performance. MLmonitoring offers a API that can be used with any existing machine learning application wherever you currently run ML code (e.g. in notebooks, standalone applications or the cloud).

## Installation

Install MLmonitoring from PyPI via

```bash
pip install git+git://github.com/rodrigoazs/monitoring.git
```

Set the MLMONITORING_DATABASE_URI enviroment variable a SQL Alchemy URI in the following way:

```bash
<dialect>+<driver>://<username>:<password>@<host>:<port>/<database
```

For more details, see [SQLAlchemy database URI](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls).

And the start the server

```bash
mlmonitoring --host 0.0.0.0 -p 8000
```

## Usage

The example scripts show how the MLmonitoring API can be used to track the model perfomance.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Why monitoring?

How can we know if the models are behaving as we expect them to? What if the behavior of customers or individuals change over the time and the training data is too old for the production data? The monitoring of machine learning models refers to ways to track and understand models performance.

An inadequate monitoring can lead to incorrect models left unchecked in production, out of date models that stop adding business value, or bugs in models that appear over time and never get caught. 

There are distinct phases in the lifecycle of an ML model. The final phase is Monitoring and Observability, where we ensure our model is doing what we expect it to in production.

![Source: martinfowler.com](https://christophergs.com/assets/images/monitoring/rsz_cd4ml.png)

Monitoring can be divided in two different parts: Data Science issues, statistical tests on model inputs and output; and Operational issues, system health, latency, memory/CPU/disk utilization. This platform focus in monitoring drifts in ML models and its predictive performance.

The monitoring results can be visualized in any data visualization you like such as Grafana, Kibana, Apache Superset or Metabase.

![Source: martinfowler.com](https://i.imgur.com/Vram3ui.png)
