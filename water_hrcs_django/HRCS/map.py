import os
import googlemaps


class Geocoding:

    def __init__(self):
        self.key = 'AIzaSyC9OYTu-eCoyoAKfUsFabZx-k-yA_Wg8fw'
        self.client = googlemaps.Client(key=self.key)

    def geocode(self, _location):
        try:
            json = googlemaps.client.geocode(self.client, _location, language='zh-TW')
            location = json[0]['geometry']['location']
            return location
        except IndexError:
            raise Exception("請輸入有效地址!")

    def decode(self, _location):
        try:
            json = googlemaps.client.reverse_geocode(self.client, _location, language='zh-TW')
            location = json[0]['geometry']['location']
            return location
        except googlemaps.exceptions.HTTPError:
            raise Exception("請輸入有效座標!")
