#!/usr/bin/env python3

import requests, logging, json
from ..security.enviroment import env_variable
import asyncio
from typing import Optional

"""
Documentation Page: 
https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search
"""


headers = {
    "accept": "application/vnd.amadeus+json",
    "Authorization": f"Bearer {env_variable['AMADEUS_ACCES_TOKEN']}"
}



class amadeus_auth:

    def __init__(self):
        self.URL_BASE  = "https://test.api.amadeus.com/v1"

    def generate_acess_token(self):
        """Generates an acces token"""
        url = self.URL_BASE + "/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = f"grant_type=client_credentials&client_id={env_variable['AMADEUS_API_KEY']}&client_secret={env_variable['AMADEUS_API_SECRET']}"

        response = requests.post(url, headers=headers, data=data)
        print(response.json())
        
        if response.status_code == 200:
            print("Acces token generated")
            env_variable["AMADEUS_ACCES_TOKEN"] = response.json().get("access_token")
        else:
            raise ValueError(f"An error ocurred: {response.json()['error_description']}")



class flights_handler(amadeus_auth):

    def __init__(self):
        super().__init__()
        self.URL_BASE_SERVICE = "https://test.api.amadeus.com/v2"
    
    def get_IATA_code(self, city):
        pass

    def get_city_fromn_IATA(self, iata_code):
        pass

    def get_flights_offer(
            self, originLocationCode: str, destinationLocationCode: str, departureDate: str, adults: Optional[str] = 1,
            returnDate: Optional[str] = None, children: Optional[str] = 0, infants: Optional[str] = None,
            travelClass: Optional[str] = None, includedAirlineCodes: Optional[str] = None, excludedAirlineCodes: Optional[str] = None,
            nonStop: Optional[str] = 'false', currencyCode: Optional[str] = 'EUR', maxPrice: Optional[int] = None, max: Optional[int] = 10
        ):
        url = self.URL_BASE_SERVICE + "/shopping/flight-offers"
        
        request_body = {
            "originLocationCode": originLocationCode,
            "destinationLocationCode": destinationLocationCode,
            "departureDate": departureDate,
            "adults": adults,
            "returnDate": returnDate,
            "children": children,
            "infants": infants,
            "travelClass": travelClass,
            "includedAirlineCodes": includedAirlineCodes,
            "excludedAirlineCodes": excludedAirlineCodes,
            "nonStop": nonStop,
            "currencyCode": currencyCode,
            "maxPrice": maxPrice,
            "max": max
        }

        self.generate_acess_token()

        headers = {
            "accept": "application/vnd.amadeus+json",
            "Authorization": f"Bearer {env_variable['AMADEUS_ACCES_TOKEN']}"
        }

        logging.info("Searching for a flight..")
        response = dict(requests.get(url, headers=headers, params=request_body).json())
        
        # Extract relevant data
        flight_data = []
        for flight_offer in response['data']:
            flight_details = {}
            flight_details['id'] = flight_offer['id']
            flight_details['source'] = flight_offer['source']
            flight_details['total_price'] = flight_offer['price']['total']
            
            # Extract itinerary details
            itineraries = []
            for itinerary in flight_offer['itineraries']:
                segments = []
                for segment in itinerary['segments']:
                    segment_details = {
                        'departure': segment['departure']['iataCode'],
                        'arrival': segment['arrival']['iataCode'],
                        'carrier': segment['carrierCode'],
                        'departure_time': segment['departure']['at'],
                        'arrival_time': segment['arrival']['at'],
                        'duration': segment['duration']
                    }
                    segments.append(segment_details)
                itineraries.append(segments)
            
            flight_details['itineraries'] = itineraries
            flight_data.append(flight_details)

        # Display extracted data
        print(json.dumps(flight_data, indent=2))
        






def get_IATA_code(city):
    pass

def get_flights():
    """"""
    pass



if __name__ == "__main__":

    # generate_acess_token()
    print(env_variable["AMADEUS_ACCES_TOKEN"])

    flights = flights_handler()
    print(flights.get_flights_offer("BCN", "BOS", "2024-05-02", "2"))
