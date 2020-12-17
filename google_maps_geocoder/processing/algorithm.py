# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.analysis import QgsBatchGeocodeAlgorithm
from qgis.core import QgsGoogleMapsGeocoder


class GoogleMapsBatchGeocode(QgsBatchGeocodeAlgorithm):

    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region
        self.coder = QgsGoogleMapsGeocoder(api_key, self.region)
        QgsBatchGeocodeAlgorithm.__init__(self, self.coder)

    def groupId(self):
        return None

    def group(self):
        return None

    def name(self):
        return 'google_maps_geocode'

    def displayName(self):
        return 'Google Maps batch geocoder'

    def createInstance(self):
        return GoogleMapsBatchGeocode(self.api_key, self.region)
