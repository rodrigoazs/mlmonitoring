from pydantic import BaseModel


class InsertModel(BaseModel):
    table_name: str
    dataframe: dict = {}

    class Config:
        schema_extra = {
            "insert": {
                "table_name": "Table name",
                "dataframe": {"Key": "Value"},
            }
        }
