# -*- coding: utf-8 -*-

# /***************************************************************************
# gui_utils.py
# ----------
# Date                 : September 2019
# copyright            : (C) 2019 by Nyall Dawson
# email                : nyall.dawson@gmail.com
#
#  ***************************************************************************/
#
# /***************************************************************************
#  *                                                                         *
#  *   This program is free software; you can redistribute it and/or modify  *
#  *   it under the terms of the GNU General Public License as published by  *
#  *   the Free Software Foundation; either version 2 of the License, or     *
#  *   (at your option) any later version.                                   *
#  *                                                                         *
#  ***************************************************************************/

"""
GUI Utilities
"""


import os
from qgis.PyQt.QtGui import QIcon


class GuiUtils:
    """
    Utilities for GUI plugin components
    """

    @staticmethod
    def get_icon(icon: str):
        """
        Returns a plugin icon.svg
        :param icon: icon.svg name (svg file name)
        :return: QIcon
        """
        path = GuiUtils.get_icon_path(icon)
        if not path:
            return QIcon()

        return QIcon(path)

    @staticmethod
    def get_icon_path(icon: str):
        """
        Returns a plugin icon.svg path
        :param icon: icon.svg name (svg file name)
        :return: icon.svg path
        """
        path = os.path.join(
            os.path.dirname(__file__),
            'images',
            icon)
        if not os.path.exists(path):
            return ''

        return path

    @staticmethod
    def get_ui_path(file: str):
        """
        Returns a UI file path
        :param file: UI file name
        :return: full UI file path
        """
        path = os.path.join(
            os.path.dirname(__file__),
            'ui',
            file)
        if not os.path.exists(path):
            return ''

        return path
