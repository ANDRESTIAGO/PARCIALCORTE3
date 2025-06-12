from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from models import *
from operaciones_boleto import *

from app import home 

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home.router)

templates = Jinja2Templates(directory="templates")

@app.get("allflyes", response_model=list[boleto_id])
async def get_all_fly():
    