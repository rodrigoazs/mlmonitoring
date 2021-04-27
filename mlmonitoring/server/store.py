import os
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
