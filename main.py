from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app import home 

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home.router)

<<<<<<< HEAD
<<<<<<< HEAD
templates = Jinja2Templates(directory="templates")

=======
templates = Jinja2Templates(directory="templates")
>>>>>>> f787baee20d09023a87bbb577c15185707d198b6
=======
templates = Jinja2Templates(directory="templates")
>>>>>>> 2129e2d60c50b3d725a5e785174412c9ede6bff0
