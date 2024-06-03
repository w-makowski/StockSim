from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout,
                               QLabel,
                               QFrame,
                               QHBoxLayout,
                               QPushButton)
from PySide6.QtCharts import QChart, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from gui.stock_chart_view import StockChartView


class StockView(QWidget):
    def __init__(self, main_controller):
        super().__init__()

        self.main_controller = main_controller
        self.controller = None

        self.setWindowTitle("Stock")

        self.back_button = QPushButton("Back", self)
        self.back_button.setMinimumWidth(90)

        self.stock_summary_board = QFrame(self)
        self.stock_summary_board.setStyleSheet("""
                            QFrame {
                                background-color: #212121;
                                border-radius: 18px;
                            }
                        """)

        self.stock_summary_board_layout = QVBoxLayout()

        font = QFont()

        self.stock_name_label = QLabel(self)
        font.setPointSize(25)
        self.stock_name_label.setFont(font)

        self.stock_value_label = QLabel(self)
        font.setPointSize(30)
        self.stock_value_label.setFont(font)

        self.stock_diff_label = QLabel(self)
        font.setPointSize(25)
        self.stock_diff_label.setFont(font)

        self.current_volume_label = QLabel(self)
        font.setPointSize(25)
        self.current_volume_label.setFont(font)

        self.stock_value_layout = QHBoxLayout()
        self.stock_value_layout.addWidget(self.stock_value_label, alignment=Qt.AlignLeft)
        self.stock_value_layout.addWidget(self.stock_diff_label, alignment=Qt.AlignLeft)
        self.stock_value_layout.addWidget(self.current_volume_label, alignment=Qt.AlignRight)

        self.stock_summary_board_layout.addWidget(self.stock_name_label)
        self.stock_summary_board_layout.addLayout(self.stock_value_layout)

        self.stock_summary_board.setLayout(self.stock_summary_board_layout)

        self.one_day_button = QPushButton("1D", self)
        self.five_day_button = QPushButton("5D", self)
        self.three_months_button = QPushButton("3M", self)
        self.six_months_button = QPushButton("6M", self)
        self.ytd_button = QPushButton("YTD", self)
        self.one_year_button = QPushButton("1Y", self)
        self.five_years_button = QPushButton("5Y", self)
        self.all_button = QPushButton("All", self)

        self.buy_button = QPushButton("Buy", self)
        self.buy_button.setMinimumWidth(90)

        self.chart_buttons_layout = QHBoxLayout()
        self.chart_buttons_layout.addWidget(self.one_day_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.addWidget(self.five_day_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.addWidget(self.three_months_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.addWidget(self.six_months_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.addWidget(self.ytd_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.addWidget(self.one_year_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.addWidget(self.five_years_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.addWidget(self.all_button, alignment=Qt.AlignLeft)
        self.chart_buttons_layout.setAlignment(Qt.AlignLeft)

        self.middle_layout = QHBoxLayout()
        self.middle_layout.addLayout(self.chart_buttons_layout)
        self.middle_layout.addWidget(self.buy_button, alignment=Qt.AlignRight)

        self.chart_view = StockChartView(self)

        layout = QVBoxLayout()
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.stock_summary_board)
        layout.addLayout(self.middle_layout)
        layout.addWidget(self.chart_view)

        self.setLayout(layout)

    def set_controller(self, controller):
        self.controller = controller

    def connect_buttons(self):
        self.back_button.clicked.connect(self.main_controller.show_dashboard_view)
        self.one_day_button.clicked.connect(self.show_1d_chart)
        self.five_day_button.clicked.connect(self.show_5d_chart)
        self.three_months_button.clicked.connect(self.show_3m_chart)
        self.six_months_button.clicked.connect(self.show_6m_chart)
        self.ytd_button.clicked.connect(self.show_ytd_chart)
        self.one_year_button.clicked.connect(self.show_1y_chart)
        self.five_years_button.clicked.connect(self.show_5y_chart)
        self.all_button.clicked.connect(self.show_all_chart)
        self.buy_button.clicked.connect(self.controller.handle_buy_stock)

    def update_chart(self, data, stock_symbol, period):
        series = QLineSeries()
        for index, value in data.iterrows():
            timestamp = int(index.timestamp()) * 1000  # QDateTime expects milliseconds
            series.append(timestamp, value['Close'])

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"{stock_symbol} Stock Price - {period}")

        axis_x = QDateTimeAxis()
        if period in ['1d', '5d']:
            axis_x.setFormat("dd-MM-yyyy h:mm:ss")
            self.chart_view.set_format("dd-MM-yyyy h:mm:ss")
        else:
            axis_x.setFormat("dd-MM-yyyy")
            self.chart_view.set_format("dd-MM-yyyy")
        axis_x.setTitleText("Date")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Price")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart_view.setChart(chart)
        self.chart_view.set_series(series)

    def set_stock_name(self, stock_symbol, stock_name):
        self.stock_name_label.setText(f'{stock_name} ({stock_symbol})')

    def set_stock_value(self, stock_value, value_diff, value_diff_percent):
        if value_diff < 0:
            sign = ''
            self.stock_diff_label.setStyleSheet("color: red;")
        else:
            sign = '+'
            if value_diff == 0:
                self.stock_diff_label.setStyleSheet("color: white;")
            else:
                self.stock_diff_label.setStyleSheet("color: green;")
        value_diff_percent = round(value_diff_percent, 2)
        self.stock_value_label.setText(f'${stock_value}')
        self.stock_diff_label.setText(f'{sign}{value_diff} ({sign}{value_diff_percent}%)')

    def set_stock_volume(self, stock_volume):
        self.current_volume_label.setText(f"Volume: {stock_volume}")

    def show_1d_chart(self):
        # get data from 1 day
        self.controller.refresh_chart('1d')

    def show_5d_chart(self):
        # get data from 5 days
        self.controller.refresh_chart('5d')

    def show_3m_chart(self):
        # get data from 3 months
        self.controller.refresh_chart('3mo')

    def show_6m_chart(self):
        # get data from 6 months
        self.controller.refresh_chart('6mo')

    def show_ytd_chart(self):
        # get ytd data
        self.controller.refresh_chart('ytd')

    def show_1y_chart(self):
        # get data from 1 year
        self.controller.refresh_chart('1y')

    def show_5y_chart(self):
        # get data from 5 years
        self.controller.refresh_chart('5y')

    def show_all_chart(self):
        # get all data
        self.controller.refresh_chart('max')
