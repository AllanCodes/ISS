# A simple module that grabs data about the ISS
import requests
from geopy.geocoders import Nominatim


class ISSask():
    """A class to find the current ISS location, pass times, and number of people in space. """
    def __init__(self):
        self.base_url = "http://api.open-notify.org/"
        self.current_location = "iss-now"
        self.pass_times = "iss-pass"
        self.current_people = "astros"
        self.geolocator = Nominatim()

    def grabLocation(self) -> dict:
        """returns a dictionary including the latitude and longitude of the position of the ISS"""
        r = requests.get(self.base_url + self.current_location)
        if (r.status_code == 200):
            return r.json()["iss_position"]

    def grabHumans(self) -> dict:
        """returns a dictionary including the people, their location in space, and the total number of humans"""
        r = requests.get(self.base_url + self.current_people)
        if (r.status_code == 200):
            return r.json()["people"]

    def getPassTimes(self, latitude=None, longitude=None, **opts) -> dict:
        """returns a dictionary including the number of passes and the corresponding durations/risetimes
        Args:
            latitude: default 0
            longitude: default 0
            If default values you must pass a string called location including the city/state"""

        pars = {"lat": latitude, "lon": longitude}
        # lat and lon aren't supplied, use location given
        if latitude is None and longitude is None:
            if 'location' in opts:
                loc = self.geolocator.geocode(opts['location'])
                pars['lat'] = loc.latitude
                pars['lon'] = loc.longitude
            else:
                raise ValueError("If no latitude/longitude must provide location=city/state ")
        r = requests.get(self.base_url + self.pass_times + ".json", params=pars)
        if (r.status_code == 200):
            ret = {}
            ret["passes"] = r.json()['request']['passes']
            ret["passtimes"] = r.json()['response']
            return ret
