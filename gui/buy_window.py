from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox, QSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class BuyWindow(QDialog):
    def __init__(self, parent=None, buy_controller=None):
        super().__init__(parent)
        self.setWindowTitle("Buy Stocks")

        self.setFixedSize(550, 550)

        self.parent = parent
        self.buy_controller = buy_controller

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setStyleSheet("""
                    QFrame {
                        background-color: #212121;
                        border-radius: 15px;
                    }
                """)
        self.frame.setFixedSize(450, 450)

        frame_layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(30)

        self.stock_name_label = QLabel(self)
        self.stock_name_label.setFont(font)

        self.stock_current_price_label = QLabel(self)
        font.setPointSize(22)
        self.stock_current_price_label.setFont(font)

        self.stock_current_volume_label = QLabel(self)
        self.stock_current_volume_label.setFont(font)

        self.select_amount_label = QLabel("Select stock amount:", self)
        self.select_amount_label.setFont(font)

        self.stock_amount_selector = QSpinBox(self)
        self.stock_amount_selector.setMinimum(0)
        self.stock_amount_selector.setSingleStep(1)
        self.stock_amount_selector.setValue(0)
        self.stock_amount_selector.valueChanged.connect(self.handle_value_changed)
        self.stock_amount_selector.setFixedSize(100, 40)
        self.stock_amount_selector.setFont(font)

        self.stock_total_price = QLabel("Total:", self)
        self.stock_total_price.setFont(font)

        self.cancel_button = QPushButton("Cancel", self)
        self.buy_button = QPushButton("Buy", self)
        self.buy_button.setEnabled(False)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.buy_button)
        self.buttons_layout.setAlignment(Qt.AlignBottom)

        frame_layout.addWidget(self.stock_name_label, alignment=Qt.AlignTop)
        frame_layout.addSpacing(45)
        frame_layout.addWidget(self.stock_current_price_label)
        frame_layout.addWidget(self.stock_current_volume_label)
        frame_layout.addSpacing(20)
        frame_layout.addWidget(self.select_amount_label, alignment=Qt.AlignHCenter)
        frame_layout.addWidget(self.stock_amount_selector, alignment=Qt.AlignHCenter)
        frame_layout.addSpacing(30)
        frame_layout.addWidget(self.stock_total_price, alignment=Qt.AlignHCenter)
        frame_layout.addSpacing(30)
        frame_layout.addLayout(self.buttons_layout)
        frame_layout.setAlignment(Qt.AlignCenter)

        self.frame.setLayout(frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def toggle_buy_button(self):
        condition = int(self.stock_amount_selector.value()) > 0
        self.buy_button.setEnabled(condition)

    def handle_value_changed(self):
        self.toggle_buy_button()
        self.buy_controller.calculate_total_price(self.stock_amount_selector.value())

    def set_controller(self, buy_controller):
        self.buy_controller = buy_controller

    def connect_buttons(self):
        self.cancel_button.clicked.connect(self.close)
        self.buy_button.clicked.connect(self.accept_payment)

    def set_stock_current_price(self, stock_price):
        self.stock_current_price_label.setText(f"Current price:\t${stock_price}")

    def set_stock_current_volume(self, stock_volume):
        self.stock_current_volume_label.setText(f"Current volume:\t{stock_volume}")
        self.stock_amount_selector.setMaximum(stock_volume)

    def set_buy_stock_name(self, stock_symbol, stock_name):
        self.stock_name_label.setText(f'{stock_name}\n({stock_symbol})')

    def set_total_price(self, total_price):
        self.stock_total_price.setText(f"Total: ${total_price}")

    def show_purchase_failure_message(self):
        QMessageBox().warning(self, "Insufficient funds", "Insufficient funds!")

    def show_purchase_successful_message(self):
        QMessageBox().warning(self, "Successful purchase", "Successful purchase!")

    def refresh_stock_amount_selector(self):
        self.stock_amount_selector.setMinimum(0)
        self.stock_amount_selector.setSingleStep(1)
        self.stock_amount_selector.setValue(0)

    def accept_payment(self):
        self.buy_controller.accept_purchase(self.stock_amount_selector.value(), self.buy_controller.current_price)
