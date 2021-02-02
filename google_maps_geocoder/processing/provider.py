# -*- coding: utf-8 -*-

"""
***************************************************************************
    provider.py
    ---------------------
    Date                 : February 2020
    Copyright            : (C) 2020 by Nyall Dawson
    Email                : nyall dot dawson at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProcessingProvider

from google_maps_geocoder.processing.algorithm import (
    GoogleMapsBatchGeocode
)
from google_maps_geocoder.gui.gui_utils import GuiUtils


class GoogleMapsProvider(QgsProcessingProvider):
    """
    Processing provider for Google Maps
    """

    def __init__(self):
        super().__init__()
        self.algs = []
        self.region = None
        self.api_key = None

    def icon(self):
        """
        Returns the provider's icon
        """
        return GuiUtils.get_icon("icon.svg")

    def svgIconPath(self):
        """
        Returns a path to the provider's icon as a SVG file
        """
        return GuiUtils.get_icon_svg("icon.svg")

    def name(self):
        """
        Display name for provider
        """
        return self.tr('Google maps')

    def versionInfo(self):
        """
        Provider plugin version
        """
        return "0.0.3"

    def id(self):
        """
        Unique ID for provider
        """
        return 'googlemaps'

    def set_config(self, api_key, region):
        """
        Sets the api key
        """
        self.api_key = api_key
        self.region = region
        self.refreshAlgorithms()

    def loadAlgorithms(self):
        """
        Called when provider must populate its available algorithms
        """
        self.addAlgorithm(GoogleMapsBatchGeocode(self.api_key, self.region))

    def tr(self, string, context=''):
        """
        Translates a string
        """
        if context == '':
            context = 'GoogleMaps'
        return QCoreApplication.translate(context, string)
