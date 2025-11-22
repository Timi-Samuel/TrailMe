import requests
import os
from abc import ABC, abstractmethod
from custom_exceptions import InvalidTravelModeError

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

API_KEY = os.getenv('GOOGLE_API_KEY')


class MapService(ABC):
    def __init__(self, olat, olong, dlat, dlong):
        self.olat = olat
        self.olong = olong
        self.dlat = dlat
        self.dlong = dlong

    @staticmethod
    def get_headers():
        return {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.legs.steps"}

    @abstractmethod
    def get_payload(self):
        pass

    def make_post(self):
        headers = self.get_headers()
        payload = self.get_payload()
        response = requests.post(url=url, json=payload, headers=headers)
        return response

    def get_trip_details(self):
        response = self.make_post()
        total_distance = response.json()['routes'][0]['distanceMeters']
        estimate_travel_time = response.json()['routes'][0]['duration']

        steps = response.json()['routes'][0]['legs'][0]['steps']
        instructions = [
            i.get('navigationInstruction', {}).get('instructions', '')
            for i in steps
            if 'navigationInstruction' in i
        ]
        distance_between_turns = [i["localizedValues"]
                                  ['distance']['text'] for i in steps]
        time_between_turns = [i["staticDuration"]['text'] for i in steps]

        return {'total_distance': total_distance, 'estimate_travel_time': estimate_travel_time, 'instructions': instructions, 'distance_between_turns': distance_between_turns, 'time_between_turns': time_between_turns}

    def format_trip_details(self):
        details = self.get_trip_details()
        formatted_details = {'total_distance': details['total_distance'],
                             'estimate_travel_time': details['estimate_travel_time'], 'formatted_list': []}
        for i, instruction in enumerate(details['instructions']):
            formatted = f"In roughly {details['distance_between_turns'][i]} (Roughly {details['time_between_turns'][i]}), {instruction}"
            formatted_details['formatted_list'].append(formatted)
        return formatted_details


class WalkService(MapService):
    def __init__(self, olat, olong, dlat, dlong):
        super().__init__(olat, olong, dlat, dlong)

    def get_payload(self):
        return {
            "origin": {"location": {"latLng": {"latitude": self.olat, "longitude": self.olong}}},
            "destination": {"location": {"latLng": {"latitude": self.dlat, "longitude": self.dlong}}},
            "travelMode": "WALK",
            "languageCode": "en"}

    def get_format_trip_details(self):
        return self.format_trip_details()


class DriveService(MapService):
    def __init__(self, olat, olong, dlat, dlong):
        super().__init__(olat, olong, dlat, dlong)

    def get_payload(self):
        return {
            "origin": {"location": {"latLng": {"latitude": self.olat, "longitude": self.olong}}},
            "destination": {"location": {"latLng": {"latitude": self.dlat, "longitude": self.dlong}}},
            "travelMode": "DRIVE",
            "languageCode": "en"}

    def get_format_trip_details(self):
        return self.format_trip_details()


class TravelModeSelector:
    def __init__(self, olat, olong, dlat, dlong, travel_type):
        self.olat = olat
        self.olong = olong
        self.dlat = dlat
        self.dlong = dlong
        self.travel_type = travel_type

    def travel_details(self):
        if self.travel_type.lower() == 'walk':
            return WalkService(self.olat, self.olong, self.dlat, self.dlong).get_format_trip_details()
        elif self.travel_type.lower() == 'drive':
            return DriveService(self.olat, self.olong, self.dlat, self.dlong).get_format_trip_details()
        else:
            raise InvalidTravelModeError(
                "Invalid Travel Mode. Choose between 'drive' or 'walk'.")
