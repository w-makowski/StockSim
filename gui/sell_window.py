from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
                               QMessageBox, QSpinBox, QScrollArea, QWidget, QSizePolicy,
                               QWidgetItem, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SellWindow(QDialog):
    def __init__(self, parent=None, sell_controller=None):
        super().__init__(parent)
        self.setWindowTitle("Sell Stocks")

        self.setFixedSize(650, 650)

        self.parent = parent
        self.sell_controller = sell_controller

        font = QFont()

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setStyleSheet("""
                            QFrame {
                                background-color: #212121;
                                border-radius: 15px;
                            }
                        """)
        self.frame.setFixedSize(500, 500)

        frame_layout = QVBoxLayout()

        font.setPointSize(30)

        self.choose_stocks_label = QLabel("Choose stocks to sell:", self)
        self.choose_stocks_label.setFont(font)

        self.sell_stocks_list = QListWidget(self)
        self.sell_stocks_list.setSelectionBehavior(QListWidget.SelectRows)
        self.sell_stocks_list.setSelectionMode(QListWidget.SingleSelection)
        self.sell_stocks_list.setHorizontalScrollMode(QListWidget.ScrollPerPixel)

        self.sell_stocks_list.itemClicked.connect(self.handle_selecting_sell_stock)

        self.sell_stock_name = QLabel(self)
        self.sell_stock_name.setFont(font)
        font.setPointSize(20)
        self.current_stock_price = QLabel("Current stock price:", self)
        self.current_stock_price.setFont(font)

        self.sell_stock_amount_selector = QSpinBox(self)
        self.sell_stock_amount_selector.setMinimum(0)
        self.sell_stock_amount_selector.setSingleStep(1)
        self.sell_stock_amount_selector.setValue(0)
        self.sell_stock_amount_selector.valueChanged.connect(self.handle_value_changed)
        self.sell_stock_amount_selector.setFixedSize(100, 40)
        font.setPointSize(25)
        self.sell_stock_amount_selector.setFont(font)

        font.setPointSize(20)
        self.sell_total_price = QLabel("Total:\t$0.00", self)
        self.sell_total_price.setFont(font)

        self.cancel_button = QPushButton("Cancel", self)
        self.sell_button = QPushButton("Sell", self)
        self.sell_button.setEnabled(False)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.sell_button)
        self.buttons_layout.setAlignment(Qt.AlignBottom)

        frame_layout.addWidget(self.choose_stocks_label)

        self.sell_stock_info_layout = QVBoxLayout()
        self.sell_stock_info_layout.addWidget(self.sell_stock_name, alignment=Qt.AlignHCenter)
        self.sell_stock_info_layout.addWidget(self.current_stock_price)
        self.sell_stock_info_layout.addWidget(self.sell_stock_amount_selector)
        self.sell_stock_info_layout.addWidget(self.sell_total_price)

        self.stock_selector_layout = QHBoxLayout()
        self.stock_selector_layout.addWidget(self.sell_stocks_list)
        self.stock_selector_layout.addLayout(self.sell_stock_info_layout)

        frame_layout.addLayout(self.stock_selector_layout)
        frame_layout.addLayout(self.buttons_layout)

        self.frame.setLayout(frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def connect_buttons(self):
        self.cancel_button.clicked.connect(self.close)
        self.sell_button.clicked.connect(self.accept_sell)

    def toggle_accept_button(self):
        condition = self.sell_stock_amount_selector.value() > 0
        self.sell_button.setEnabled(condition)

    def handle_value_changed(self):
        self.toggle_accept_button()
        total_price = str(self.sell_controller.calculate_total_price(self.sell_stock_name.text(),
                                                                     self.sell_stock_amount_selector.value()))
        self.sell_total_price.setText(f'Total:\t${total_price}')

    def set_sell_controller(self, sell_controller):
        self.sell_controller = sell_controller

    def refresh_sell_list(self, stock_data):
        self.sell_stocks_list.clear()
        for key, value in stock_data.items():
            self.sell_stocks_list.addItem(QListWidgetItem(str(value['amount']) + "\t" + key + "\t" + value['name']))

    def handle_selecting_sell_stock(self):
        self.refresh_selector()
        selected_stock = self.sell_stocks_list.selectedItems()[0]
        split_selected_stock = selected_stock.text().split("\t")
        self.sell_stock_name.setText(split_selected_stock[1])
        self.current_stock_price.setText(
            f"Current stock price:\n${self.sell_controller.get_sell_stock_current_price(split_selected_stock[1])}")
        self.sell_stock_amount_selector.setMaximum(int(split_selected_stock[0]))

    def refresh_selector(self):
        self.sell_stock_amount_selector.setMinimum(0)
        self.sell_stock_amount_selector.setSingleStep(1)
        self.sell_stock_amount_selector.setValue(0)
        self.sell_stock_amount_selector.setMaximum(0)

    def accept_sell(self):
        self.sell_controller.handle_sell(self.sell_stock_name.text(), self.sell_stock_amount_selector.value())

    def refresh_labels(self):
        self.sell_stock_name.setText("")
        self.current_stock_price.setText("Current stock price:")
        self.sell_total_price.setText("Total:\t$0.00")
