import os
import re
import json
import sqlalchemy
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
from mlmonitoring.server.schemas import InsertModel


# the server reads an environment varible
# to set the SQLAlchemy connector.
CONNECTION = os.environ.get("MLMONITOR_DATABASE_URI")
engine = sqlalchemy.create_engine(CONNECTION)


def insert_table(data: InsertModel) -> None:
    """Insert the pandas dataframe to the database table.

    Args:
        data (InsertModel): An InsertModel with
        table_name and dataframe.
    """

    # converts json to pandas dataframe
    dataframe = pd.read_json(json.dumps(data.dataframe), orient='table')

    # creates the database if it does
    # not exist
    if not database_exists(engine.url):
        create_database(engine.url)

    # save the dataframe to the sql table
    dataframe.to_sql(
        name=data.table_name,
        con=engine,
        if_exists="append",
        method="multi",
    )


def view_table(table_name: str) -> pd.DataFrame:
    """Returns the dataframe stored in the
    database table.

    Args:
        table_name (str): The name of the database table.

    Returns:
        pd.DataFrame: The table as Pandas DataFrame.
    """

    # read the table from the database
    data = pd.read_sql("SELECT * FROM {}".format(table_name), engine)

    # convert to JSON as records orientation
    dataframe = data.to_json(orient="records")

    return dataframe


def filter_table(table_name: str, query_string: str) -> pd.DataFrame:
    """Returns the dataframe stored in the
    database table filtered by a query.

    Args:
        table_name (str): The name of the database table.
        query_string (str): A query string.

    Returns:
        pd.DataFrame: The table as Pandas DataFrame.
    """

    # mapping string to sql conditionals
    mapping = {
        'gt': '>',
        'ge': '>=',
        'lt': '<',
        'le': '<=',
        'eq': '=',
        'ne': '<>',
    }

    # matchs query string
    match = re.findall(
        r'([\w]*)\_\_([\w]*)\_\_([\w.-]*)',
        query_string
    )

    sql_query = []
    for query in match:
        sql_filter = '{} {} {}'.format(
            query[0],
            mapping[query[1]],
            query[2]
        )
        sql_query.append(sql_filter)
    sql_query = ' AND '.join(sql_query)

    # read the table from the database
    data = pd.read_sql(
        "SELECT * FROM {} WHERE {}".format(table_name, sql_query),
        engine
    )

    # convert to JSON as records orientation
    dataframe = data.to_json(orient="records")

    return dataframe
