from omdb import OMDBClient
import requests
import json
import os
import environ
env = environ.Env()
environ.Env.read_env()
OMDB_KEY = env('OMDB')
client = OMDBClient(apikey=OMDB_KEY)

res = client.request(t='True Grit', y=1969, r='json')
print(res.json())
