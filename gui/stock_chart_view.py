import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox, QLabel, QToolTip
from PySide6.QtCore import Qt, QPointF
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtGui import QPainter
from PySide6.QtCore import QDateTime
import yfinance as yf
import datetime


class StockChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.Antialiasing)
        self.series = None
        self.date_format = 'dd-MM-yyyy'

    def set_series(self, series):
        self.series = series

    def set_format(self, date_format):
        self.date_format = date_format

    def mouseMoveEvent(self, event):
        if self.series:
            pos = event.pos()
            chart_value = self.chart().mapToValue(pos, self.series)
            if self.series.pointsVector():
                nearest_point = min(self.series.pointsVector(), key=lambda point: (point.x() - chart_value.x()) ** 2)
                QToolTip.showText(event.globalPos(),
                                  f"Date: {QDateTime.fromMSecsSinceEpoch(nearest_point.x()).toString(self.date_format)}"
                                  f"\nPrice: {nearest_point.y():.2f}")
        super().mouseMoveEvent(event)
