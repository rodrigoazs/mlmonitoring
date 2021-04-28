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
