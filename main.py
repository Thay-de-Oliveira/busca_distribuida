import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from functools import lru_cache
from pymongo import MongoClient
import bson
import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_name: str = ""
    mongo_uri: str = ""
    vizinhos: list[str] = []


@lru_cache
def get_environment() -> Environment:
    return Environment()


app = FastAPI()

client = TestClient(app)


@app.get("/api/{_id}")
def get_review(_id: str):
    env = get_environment()
    print(env.database_name)
    mongo_client = MongoClient(env.mongo_uri)
    database = mongo_client[env.database_name]
    collection = database["listingsAndReviews"]
    has_local_id = collection.find_one({"_id": _id})

    if not has_local_id:
        for vizinho in env.vizinhos:
            print(f"chamando vizinho={vizinho}")
    else:
        return bson.json_util.dumps(has_local_id)
