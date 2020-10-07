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

from qgis.gui import (
    QgsGui,
    QgsCodeEditorColorScheme,
)

from qgis.PyQt.QtGui import QColor


def classFactory(iface):
    return SynthwaveSchemePlugin(iface)


class SynthwaveColorScheme(QgsCodeEditorColorScheme):
    COLORS = {
        QgsCodeEditorColorScheme.ColorRole.Default: QColor("#ffffff"),
        QgsCodeEditorColorScheme.ColorRole.Keyword: QColor("#fede5d"),
        QgsCodeEditorColorScheme.ColorRole.Class: QColor("#da4b1b"),
        QgsCodeEditorColorScheme.ColorRole.Method: QColor("#b5f0ef"),
        QgsCodeEditorColorScheme.ColorRole.Decoration: QColor("#6C71C4"),
        QgsCodeEditorColorScheme.ColorRole.Number: QColor("#f97e72"),
        QgsCodeEditorColorScheme.ColorRole.Comment: QColor("#848bbd"),
        QgsCodeEditorColorScheme.ColorRole.CommentLine: QColor("#848bbd"),
        QgsCodeEditorColorScheme.ColorRole.CommentBlock: QColor("#848bbd"),
        QgsCodeEditorColorScheme.ColorRole.Background: QColor("#292239"),
        QgsCodeEditorColorScheme.ColorRole.Cursor: QColor("#d1f5f5"),
        QgsCodeEditorColorScheme.ColorRole.CaretLine: QColor("#433465"),
        QgsCodeEditorColorScheme.ColorRole.Operator: QColor("#eee4b9"),
        QgsCodeEditorColorScheme.ColorRole.QuotedOperator: QColor("#eee4b9"),
        QgsCodeEditorColorScheme.ColorRole.Identifier: QColor("#e050ba"),
        QgsCodeEditorColorScheme.ColorRole.QuotedIdentifier: QColor("#e050ba"),
        QgsCodeEditorColorScheme.ColorRole.Tag: QColor("#72f1b8"),
        QgsCodeEditorColorScheme.ColorRole.UnknownTag: QColor("#72f1b8"),
        QgsCodeEditorColorScheme.ColorRole.SingleQuote: QColor("#848bbd"),
        QgsCodeEditorColorScheme.ColorRole.DoubleQuote: QColor("#848bbd"),
        QgsCodeEditorColorScheme.ColorRole.TripleSingleQuote: QColor("#848bbd"),
        QgsCodeEditorColorScheme.ColorRole.TripleDoubleQuote: QColor("#848bbd"),
        QgsCodeEditorColorScheme.ColorRole.MarginBackground: QColor("#585858"),
        QgsCodeEditorColorScheme.ColorRole.MarginForeground: QColor("#ffffff"),
        QgsCodeEditorColorScheme.ColorRole.SelectionBackground: QColor("#45415b"),
        QgsCodeEditorColorScheme.ColorRole.SelectionForeground: QColor("#FDF6E3"),
        QgsCodeEditorColorScheme.ColorRole.MatchedBraceBackground: QColor("#34294f66"),
        QgsCodeEditorColorScheme.ColorRole.MatchedBraceForeground: QColor("#b0d7e2"),
        QgsCodeEditorColorScheme.ColorRole.Edge: QColor("#47496f"),
        QgsCodeEditorColorScheme.ColorRole.Fold: QColor("#292239"),
        QgsCodeEditorColorScheme.ColorRole.Error: QColor("#fe4450"),
    }

    def __init__(self):
        super().__init__('synthwave', 'Synthwave')

        for role, color in self.COLORS.items():
            self.setColor(role, color)


class SynthwaveSchemePlugin:
    def __init__(self, _):
        QgsGui.codeEditorColorSchemeRegistry().addColorScheme(SynthwaveColorScheme())

    def initGui(self):
        pass

    def unload(self):
        QgsGui.codeEditorColorSchemeRegistry().removeColorScheme('synthwave')
