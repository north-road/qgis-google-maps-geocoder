# -----------------------------------------------------------
# Copyright (C) 2020 Nyall Dawson
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

from functools import partial

from qgis.PyQt import uic
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QThread
)
from qgis.PyQt.QtWidgets import (
    QPushButton
)

from qgis.core import (
    QgsGoogleMapsGeocoder,
    QgsSettings,
    Qgis
)
from qgis.gui import (
    QgsOptionsPageWidget,
    QgsGeocoderLocatorFilter,
    QgsOptionsWidgetFactory
)

from google_maps_geocoder.gui_utils import GuiUtils


def classFactory(iface):
    return GoogleMapsGeocoderPlugin(iface)


OPTIONS_WIDGET, OPTIONS_BASE = uic.loadUiType(
    GuiUtils.get_ui_path('settings.ui'))


class GoogleMapsOptionsPage(OPTIONS_WIDGET, QgsOptionsPageWidget):
    """
    Google Maps options widget
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setObjectName('GoogleMapsOptions')

        self.plugin = None

    def set_plugin(self, plugin):
        self.plugin = plugin
        self.api_key_line_edit.setText(plugin.api_key)

        self.region_combo.addItem('', '')
        for code, name in plugin.region_codes.items():
            self.region_combo.addItem(name, code)

        self.region_combo.setCurrentIndex(self.region_combo.findData(plugin.region))

    def apply(self):
        """
        Applies the new settings
        """
        self.plugin.set_api_key(self.api_key_line_edit.text())
        self.plugin.set_region(self.region_combo.currentData())


class GoogleMapsOptionsFactory(QgsOptionsWidgetFactory):
    """
    Factory class for Google Maps options widget
    """

    def __init__(self, plugin):  # pylint: disable=useless-super-delegation
        super().__init__()
        self.plugin = plugin

    def icon(self):  # pylint: disable=missing-function-docstring
        return GuiUtils.get_icon('icon.svg')

    def createWidget(self, parent):  # pylint: disable=missing-function-docstring
        page = GoogleMapsOptionsPage(parent)
        page.set_plugin(self.plugin)
        return page


class GoogleMapsGeocoderPlugin:
    def __init__(self, iface):
        self.iface = iface

        settings = QgsSettings()
        self.geocoder = None
        self.filter = None
        self.api_key = settings.value('/plugins/google_maps/api_key', '', str)
        self.region = settings.value('/plugins/google_maps/region', '', str)

        self.options_factory = None

        self.region_codes = {
            "ac": self.tr("Ascension Island"),
            "ad": self.tr("Andorra"),
            "ae": self.tr("United Arab Emirates"),
            "af": self.tr("Afghanistan"),
            "ag": self.tr("Antigua and Barbuda"),
            "ai": self.tr("Anguilla"),
            "al": self.tr("Albania"),
            "am": self.tr("Armenia"),
            "an": self.tr("Netherlands Antilles"),
            "ao": self.tr("Angola"),
            "aq": self.tr("Antarctica"),
            "ar": self.tr("Argentina"),
            "as": self.tr("American Samoa"),
            "at": self.tr("Austria"),
            "au": self.tr("Australia"),
            "aw": self.tr("Aruba"),
            "ax": self.tr("Aland Islands"),
            "az": self.tr("Azerbaijan"),
            "ba": self.tr("Bosnia and Herzegovina"),
            "bb": self.tr("Barbados"),
            "bd": self.tr("Bangladesh"),
            "be": self.tr("Belgium"),
            "bf": self.tr("Burkina Faso"),
            "bg": self.tr("Bulgaria"),
            "bh": self.tr("Bahrain"),
            "bi": self.tr("Burundi"),
            "bj": self.tr("Benin"),
            "bm": self.tr("Bermuda"),
            "bn": self.tr("Brunei Darussalam"),
            "bo": self.tr("Bolivia"),
            "br": self.tr("Brazil"),
            "bs": self.tr("Bahamas"),
            "bt": self.tr("Bhutan"),
            "bv": self.tr("Bouvet Island"),
            "bw": self.tr("Botswana"),
            "by": self.tr("Belarus"),
            "bz": self.tr("Belize"),
            "ca": self.tr("Canada"),
            "cc": self.tr("Cocos (Keeling) Islands"),
            "cd": self.tr("Congo, The Democratic Republic of the"),
            "cf": self.tr("Central African Republic"),
            "cg": self.tr("Congo, Republic of"),
            "ch": self.tr("Switzerland"),
            "ci": self.tr("Cote d'Ivoire"),
            "ck": self.tr("Cook Islands"),
            "cl": self.tr("Chile"),
            "cm": self.tr("Cameroon"),
            "cn": self.tr("China"),
            "co": self.tr("Colombia"),
            "cr": self.tr("Costa Rica"),
            "cu": self.tr("Cuba"),
            "cv": self.tr("Cape Verde"),
            "cx": self.tr("Christmas Island"),
            "cy": self.tr("Cyprus"),
            "cz": self.tr("Czech Republic"),
            "de": self.tr("Germany"),
            "dj": self.tr("Djibouti"),
            "dk": self.tr("Denmark"),
            "dm": self.tr("Dominica"),
            "do": self.tr("Dominican Republic"),
            "dz": self.tr("Algeria"),
            "ec": self.tr("Ecuador"),
            "ee": self.tr("Estonia"),
            "eg": self.tr("Egypt"),
            "eh": self.tr("Western Sahara"),
            "er": self.tr("Eritrea"),
            "es": self.tr("Spain"),
            "et": self.tr("Ethiopia"),
            "eu": self.tr("European Union"),
            "fi": self.tr("Finland"),
            "fj": self.tr("Fiji"),
            "fk": self.tr("Falkland Islands (Malvinas)"),
            "fm": self.tr("Micronesia, Federated States of"),
            "fo": self.tr("Faroe Islands"),
            "fr": self.tr("France"),
            "ga": self.tr("Gabon"),
            "gb": self.tr("United Kingdom"),
            "gd": self.tr("Grenada"),
            "ge": self.tr("Georgia"),
            "gf": self.tr("French Guiana"),
            "gg": self.tr("Guernsey"),
            "gh": self.tr("Ghana"),
            "gi": self.tr("Gibraltar"),
            "gl": self.tr("Greenland"),
            "gm": self.tr("Gambia"),
            "gn": self.tr("Guinea"),
            "gp": self.tr("Guadeloupe"),
            "gq": self.tr("Equatorial Guinea"),
            "gr": self.tr("Greece"),
            "gs": self.tr("South Georgia and the South Sandwich Islands"),
            "gt": self.tr("Guatemala"),
            "gu": self.tr("Guam"),
            "gw": self.tr("Guinea-Bissau"),
            "gy": self.tr("Guyana"),
            "hk": self.tr("Hong Kong"),
            "hm": self.tr("Heard and McDonald Islands"),
            "hn": self.tr("Honduras"),
            "hr": self.tr("Croatia/Hrvatska"),
            "ht": self.tr("Haiti"),
            "hu": self.tr("Hungary"),
            "id": self.tr("Indonesia"),
            "ie": self.tr("Ireland"),
            "il": self.tr("Israel"),
            "im": self.tr("Isle of Man"),
            "in": self.tr("India"),
            "io": self.tr("British Indian Ocean Territory"),
            "iq": self.tr("Iraq"),
            "ir": self.tr("Iran, Islamic Republic of"),
            "is": self.tr("Iceland"),
            "it": self.tr("Italy"),
            "je": self.tr("Jersey"),
            "jm": self.tr("Jamaica"),
            "jo": self.tr("Jordan"),
            "jp": self.tr("Japan"),
            "ke": self.tr("Kenya"),
            "kg": self.tr("Kyrgyzstan"),
            "kh": self.tr("Cambodia"),
            "ki": self.tr("Kiribati"),
            "km": self.tr("Comoros"),
            "kn": self.tr("Saint Kitts and Nevis"),
            "kp": self.tr("Korea, Democratic People's Republic"),
            "kr": self.tr("Korea, Republic of"),
            "kw": self.tr("Kuwait"),
            "ky": self.tr("Cayman Islands"),
            "kz": self.tr("Kazakhstan"),
            "la": self.tr("Lao People's Democratic Republic"),
            "lb": self.tr("Lebanon"),
            "lc": self.tr("Saint Lucia"),
            "li": self.tr("Liechtenstein"),
            "lk": self.tr("Sri Lanka"),
            "lr": self.tr("Liberia"),
            "ls": self.tr("Lesotho"),
            "lt": self.tr("Lithuania"),
            "lu": self.tr("Luxembourg"),
            "lv": self.tr("Latvia"),
            "ly": self.tr("Libyan Arab Jamahiriya"),
            "ma": self.tr("Morocco"),
            "mc": self.tr("Monaco"),
            "md": self.tr("Moldova, Republic of"),
            "me": self.tr("Montenegro"),
            "mg": self.tr("Madagascar"),
            "mh": self.tr("Marshall Islands"),
            "mk": self.tr("Macedonia, The Former Yugoslav Republic of"),
            "ml": self.tr("Mali"),
            "mm": self.tr("Myanmar"),
            "mn": self.tr("Mongolia"),
            "mo": self.tr("Macao"),
            "mp": self.tr("Northern Mariana Islands"),
            "mq": self.tr("Martinique"),
            "mr": self.tr("Mauritania"),
            "ms": self.tr("Montserrat"),
            "mt": self.tr("Malta"),
            "mu": self.tr("Mauritius"),
            "mv": self.tr("Maldives"),
            "mw": self.tr("Malawi"),
            "mx": self.tr("Mexico"),
            "my": self.tr("Malaysia"),
            "mz": self.tr("Mozambique"),
            "na": self.tr("Namibia"),
            "nc": self.tr("New Caledonia"),
            "ne": self.tr("Niger"),
            "nf": self.tr("Norfolk Island"),
            "ng": self.tr("Nigeria"),
            "ni": self.tr("Nicaragua"),
            "nl": self.tr("Netherlands"),
            "no": self.tr("Norway"),
            "np": self.tr("Nepal"),
            "nr": self.tr("Nauru"),
            "nu": self.tr("Niue"),
            "nz": self.tr("New Zealand"),
            "om": self.tr("Oman"),
            "pa": self.tr("Panama"),
            "pe": self.tr("Peru"),
            "pf": self.tr("French Polynesia"),
            "pg": self.tr("Papua New Guinea"),
            "ph": self.tr("Philippines"),
            "pk": self.tr("Pakistan"),
            "pl": self.tr("Poland"),
            "pm": self.tr("Saint Pierre and Miquelon"),
            "pn": self.tr("Pitcairn Island"),
            "pr": self.tr("Puerto Rico"),
            "ps": self.tr("Palestinian Territory, Occupied"),
            "pt": self.tr("Portugal"),
            "pw": self.tr("Palau"),
            "py": self.tr("Paraguay"),
            "qa": self.tr("Qatar"),
            "re": self.tr("Reunion Island"),
            "ro": self.tr("Romania"),
            "rs": self.tr("Serbia"),
            "ru": self.tr("Russian Federation"),
            "rw": self.tr("Rwanda"),
            "sa": self.tr("Saudi Arabia"),
            "sb": self.tr("Solomon Islands"),
            "sc": self.tr("Seychelles"),
            "sd": self.tr("Sudan"),
            "se": self.tr("Sweden"),
            "sg": self.tr("Singapore"),
            "sh": self.tr("Saint Helena"),
            "si": self.tr("Slovenia"),
            "sj": self.tr("Svalbard and Jan Mayen Islands"),
            "sk": self.tr("Slovak Republic"),
            "sl": self.tr("Sierra Leone"),
            "sm": self.tr("San Marino"),
            "sn": self.tr("Senegal"),
            "so": self.tr("Somalia"),
            "sr": self.tr("Suriname"),
            "st": self.tr("Sao Tome and Principe"),
            "su": self.tr("Soviet Union (being phased out)"),
            "sv": self.tr("El Salvador"),
            "sy": self.tr("Syrian Arab Republic"),
            "sz": self.tr("Swaziland"),
            "tc": self.tr("Turks and Caicos Islands"),
            "td": self.tr("Chad"),
            "tf": self.tr("French Southern Territories"),
            "tg": self.tr("Togo"),
            "th": self.tr("Thailand"),
            "tj": self.tr("Tajikistan"),
            "tk": self.tr("Tokelau"),
            "tl": self.tr("Timor-Leste"),
            "tm": self.tr("Turkmenistan"),
            "tn": self.tr("Tunisia"),
            "to": self.tr("Tonga"),
            "tp": self.tr("East Timor"),
            "tr": self.tr("Turkey"),
            "tt": self.tr("Trinidad and Tobago"),
            "tv": self.tr("Tuvalu"),
            "tw": self.tr("Taiwan"),
            "tz": self.tr("Tanzania"),
            "ua": self.tr("Ukraine"),
            "ug": self.tr("Uganda"),
            "uk": self.tr("United Kingdom"),
            "um": self.tr("United States Minor Outlying Islands"),
            "us": self.tr("United States"),
            "uy": self.tr("Uruguay"),
            "uz": self.tr("Uzbekistan"),
            "va": self.tr("Holy See (Vatican City State)"),
            "vc": self.tr("Saint Vincent and the Grenadines"),
            "ve": self.tr("Venezuela"),
            "vg": self.tr("Virgin Islands, British"),
            "vi": self.tr("Virgin Islands, U.S."),
            "vn": self.tr("Vietnam"),
            "vu": self.tr("Vanuatu"),
            "wf": self.tr("Wallis and Futuna Islands"),
            "ws": self.tr("Samoa"),
            "ye": self.tr("Yemen"),
            "yt": self.tr("Mayotte"),
            "yu": self.tr("Yugoslavia"),
            "za": self.tr("South Africa"),
            "zm": self.tr("Zambia"),
            "zw": self.tr("Zimbabwe"),
        }

    @staticmethod
    def tr(message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GoogleMapsGeocoder', message)

    def initGui(self):
        self.register()

        self.options_factory = GoogleMapsOptionsFactory(self)
        self.options_factory.setTitle(self.tr('Google Maps'))
        self.iface.registerOptionsWidgetFactory(self.options_factory)
        self.check_api_key()

    def unload(self):
        self.unregister()
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

    def unregister(self):
        if self.filter is not None:
            self.iface.deregisterLocatorFilter(self.filter)
            self.filter = None
            self.geocoder = None

    def register(self):
        if self.api_key:
            self.geocoder = QgsGoogleMapsGeocoder(self.api_key, self.region)
            self.filter = QgsGeocoderLocatorFilter('Google', 'Google', 'addr', self.geocoder, self.iface.mapCanvas())
            self.iface.registerLocatorFilter(self.filter)

    def set_api_key(self, api_key):
        settings = QgsSettings()
        settings.setValue('/plugins/google_maps/api_key', api_key)
        self.api_key = api_key
        self.unregister()
        self.register()
        self.check_api_key()

    def set_region(self, region):
        settings = QgsSettings()
        settings.setValue('/plugins/google_maps/region', region)

        self.region = region
        self.unregister()
        self.register()

    def check_api_key(self):
        """
        Checks if an API key has been entered, and warns if not.
        """
        if not self.api_key:
            if QCoreApplication.instance().thread() == QThread.currentThread():
                # Main thread, safe to create a button
                bar = self.iface.messageBar()
                widget = bar.createMessage(self.tr('Google Maps'), self.tr("No API key entered, please configure"))
                settings_button = QPushButton("Enter API Key…", pressed=partial(self.open_settings, message_bar_widget=widget))
                widget.layout().addWidget(settings_button)
                bar.pushWidget(widget, Qgis.Critical)

            return False

        return True

    def open_settings(self, message_bar_widget=None):
        """
        Opens the settings dialog at the Google Maps page
        """
        self.iface.showOptionsDialog(self.iface.mainWindow(), currentPage='GoogleMapsOptions')
        if message_bar_widget:
            self.iface.messageBar().popWidget(message_bar_widget)
