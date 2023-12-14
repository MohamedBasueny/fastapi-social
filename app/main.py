import time
from uuid import uuid4
from fastapi import Body, FastAPI, Response , status , HTTPException , Depends
import psycopg
from . import models 
from .database import engine  , get_db
from .schemas import *
from typing import List
from app.utils import * 
from .routers import post , user , auth , vote
from fastapi.middleware.cors import CORSMiddleware
##################################################Main Configuration####################################################
#comment the below line if you want alembic to generate the tables for you via --autogenerate
# models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

origins = ['*']

app.add_middleware(
    CORSMiddleware , 
    allow_origins= origins , 
    allow_headers = ['*'] , 
    allow_credentials= True , 
    allow_methods = ['*']
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

################################################helper functions#######################################################

################################################helper functions#######################################################

################################################Database connection Not ORM#######################################################
# Connect to an existing database using a sql driver 
# while True : 
#     try  : 
#         conn = psycopg.connect("dbname=fastapi host=localhost user=postgres password=0716103235")
#         cursor = conn.cursor()
#         break
#     except Exception as error : 
#         print(f"error details in connecting to DB with details \n{error}")
#         time.sleep(2)
################################################Database connection#######################################################

@app.get("/") 
async def root():
    return {"message" : "hello World!"}