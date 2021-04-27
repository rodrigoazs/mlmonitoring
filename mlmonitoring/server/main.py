import uvicorn
import click
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mlmonitoring.server.store import insert_table, view_table


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
    try:
        insert_table(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/view/{table_name}")
async def view_dataframe(table_name: str):
    return view_table(table_name)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

@click.command()
@click.option(
    '--host',
    '-h',
    default="0.0.0.0",
    help="The network address to listen on (default: 0.0.0.0)."
)
@click.option(
    '--port',
    '-p',
    default=8000,
    help="The port to listen on (default: 8000)."
)
def cli(host, port):
    click.echo('Initializing Sparkle server')
    uvicorn.run(
        "sparkle.server.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="debug"
    )
    uvicorn.run(
        app,
        host=host,
        port=port
    )
