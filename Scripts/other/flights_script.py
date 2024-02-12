import requests
import pandas as pd
import numpy as np
from pathlib import Path
import uuid
import asyncio

"""
"Objective": I'll just need to write the airport from where the airports are. And then even if the client wants to
set a date they'll be able to do it.

request data: <city> || <airport>

"""
df_main = pd.DataFrame(columns=['id', 'ciudad-origen', 'ciudad-destino', 'aeronave', 'numero_vuelo', 'precio', 'url'])


df_flights = pd.read_csv("https://travel360-images-handle.s3.eu-north-1.amazonaws.com/datasets/flights.csv")
df_airports = pd.read_csv("https://travel360-images-handle.s3.eu-north-1.amazonaws.com/datasets/airports.csv")
def_raw_flight_data = pd.read_csv("https://travel360-images-handle.s3.eu-north-1.amazonaws.com/datasets/raw-flight-data.csv")

async def fetch_ciudad_by_id(id):
    """Get origin city from id"""
    result = df_airports[df_airports["airport_id"] == id]
    if not result.empty:
        return result.iloc[0]["city"]
    else:
        return None


async def create_row(origin_city_id, destination_city_id):
    id = uuid.uuid4()
    origin_city = await fetch_ciudad_by_id(origin_city_id)
    destination_city = await fetch_ciudad_by_id(destination_city_id)

async def builder():
    pass

async def main():
    asyncio.gather()


if __name__ == "__main__":
    asyncio.run(main())