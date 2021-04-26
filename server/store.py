import os
import json
import sqlalchemy
import pandas as pd
from sqlalchemy_utils import database_exists, create_database


CONNECTION = os.environ.get("MLMONITOR_DATABASE_URI")
engine = sqlalchemy.create_engine(CONNECTION)


def insert_table(data):
    dataframe = pd.read_json(json.dumps(data.dataframe), orient='table')

    if not database_exists(engine.url):
        create_database(engine.url)

    dataframe.to_sql(
                name=data.table_name,
                con=engine,
                if_exists="append",
                method="multi",
            )


def view_table(table_name):
    data = pd.read_sql("SELECT * FROM {}".format(table_name), engine)

    dataframe = data.to_json(orient="records")
    
    return dataframe