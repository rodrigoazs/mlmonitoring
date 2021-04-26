import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from store import insert_table, view_table


app = FastAPI()


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


@app.post("/insert")
async def insert_dataframe(data: InsertModel):
    insert_table(data)


@app.get("/view/{table_name}")
async def view_dataframe(table_name: str):
    print(table_name)
    return view_table(table_name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)