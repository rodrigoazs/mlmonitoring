import uvicorn
import click
from fastapi import FastAPI, HTTPException
from mlmonitoring.server.schemas import InsertModel
from mlmonitoring.server.store import (
    insert_table,
    view_table
)


app = FastAPI()


@app.post("/insert")
async def insert_dataframe(data: InsertModel):
    try:
        insert_table(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/view/{table_name}")
async def view_dataframe(table_name: str):
    try:
        return view_table(table_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    click.echo('Initializing MLmonitoring server')
    uvicorn.run(
        app,
        host=host,
        port=port
    )
