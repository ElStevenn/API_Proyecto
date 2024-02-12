import requests
import asyncio
"""
Documentation Page: 
https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search
"""

API_Key = "gJ3BMlmCCErMiXOqAEueGi2SjMBKn4cQ"
API_Seret = "eqrLRcMnF5wXpu37"

URL_BASE = "https://test.api.amadeus.com/v1"

header = {
    "client_id":API_Key,
    "client_secret":API_Seret
}

boddy_request = {
    "originLocationCode":"BCN", #IATA code format
    "destinationLocationCode":"BOS",#IATA code format
    "departureDate":"2024-05-02",
    "adults":1
}
res = requests.get(headers=header)
print(res.json())