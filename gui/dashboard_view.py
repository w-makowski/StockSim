from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QLabel,
                               QPushButton,
                               QListWidget,
                               QMessageBox,
                               QLineEdit,
                               QListWidgetItem, QFrame, QScrollArea, QSizePolicy)
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtCore import Qt, QPoint


class DashboardView(QWidget):
    def __init__(self, main_controller):
        super().__init__()

        self.main_controller = main_controller
        self.controller = None

        self.setWindowTitle("Dashboard")

        font = QFont()
        font.setPointSize(30)
        self.user_greeting_label = QLabel(self)
        self.user_greeting_label.setFont(font)

        self.logout_button = QPushButton("Logout", self)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.user_greeting_label, alignment=Qt.AlignLeft)
        self.topLayout.addWidget(self.logout_button, alignment=Qt.AlignRight)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search stock by symbol...")
        self.search_bar.setStyleSheet("""
                    QLineEdit {
                        border: 2px solid #ccc;
                        border-radius: 10px;
                        padding: 5px;
                    }
                """)

        self.balance_board = QFrame(self)
        self.balance_board.setStyleSheet("""
                    QFrame {
                        background-color: #212121;
                        border-radius: 18px;
                    }
                """)

        self.balance_board_layout = QHBoxLayout()

        self.balance_labels_layout = QVBoxLayout()
        font.setPointSize(42)
        self.account_balance_label = QLabel("Account balance:", self)
        self.account_balance_label.setFont(font)
        self.balance_label = QLabel(self)
        self.balance_label.setFont(font)
        self.balance_labels_layout.addWidget(self.account_balance_label)
        self.balance_labels_layout.addWidget(self.balance_label)

        self.deposit_button = QPushButton('Deposit', self)

        self.balance_board_layout.addLayout(self.balance_labels_layout)
        self.balance_board_layout.addWidget(self.deposit_button, alignment=Qt.AlignRight)

        self.balance_board.setLayout(self.balance_board_layout)

        font.setPointSize(18)
        self.my_portfolio_label = QLabel("My Portfolio:", self)
        self.my_portfolio_label.setFont(font)

        self.sell_button = QPushButton("Sell", self)
        self.sell_button.setMinimumWidth(55)

        self.portfolio_label_layout = QHBoxLayout()
        self.portfolio_label_layout.addWidget(self.my_portfolio_label, alignment=Qt.AlignLeft)
        self.portfolio_label_layout.addWidget(self.sell_button, alignment=Qt.AlignRight)

        self.stock_list = QListWidget(self)
        self.stock_list.setSelectionBehavior(QListWidget.SelectRows)
        self.stock_list.setSelectionMode(QListWidget.SingleSelection)

        self.most_gains_area = QScrollArea()
        self.most_gains_area.setMaximumHeight(70)
        self.most_gains_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.most_gains_area.setWidgetResizable(True)

        self.most_gains_widget = QWidget(self)
        self.most_gains_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.most_gains_layout = QHBoxLayout()
        self.most_gains_widget.setLayout(self.most_gains_layout)

        self.most_gains_items = []

        for i in range(20):
            stock_item = StockItem("", "", "")
            self.most_gains_items.append(stock_item)
            self.most_gains_layout.addWidget(stock_item)

        self.most_gains_area.setWidget(self.most_gains_widget)

        self.most_volume_area = QScrollArea()
        self.most_volume_area.setMaximumHeight(70)
        self.most_volume_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.most_volume_area.setWidgetResizable(True)

        self.most_volume_widget = QWidget(self)
        self.most_volume_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.most_volume_layout = QHBoxLayout()
        self.most_volume_widget.setLayout(self.most_volume_layout)

        self.most_volume_items = []

        for i in range(20):
            stock_item = StockItem("", "", "")
            self.most_volume_items.append(stock_item)
            self.most_volume_layout.addWidget(stock_item)

        self.most_volume_area.setWidget(self.most_volume_widget)

        layout = QVBoxLayout()
        layout.addLayout(self.topLayout)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.balance_board)
        layout.addLayout(self.portfolio_label_layout)
        layout.addWidget(self.stock_list)
        layout.addWidget(self.most_gains_area)
        layout.addWidget(self.most_volume_area)

        self.suggestion_list = QListWidget(self)
        self.suggestion_list.setMaximumHeight(100)
        self.suggestion_list.setVisible(False)

        self.setLayout(layout)

    def set_user_balance(self, balance):
        self.balance_label.setText(f'${balance}')

    def update_most_gains(self, sample_data):
        for index, (symbol, price, gain_value, gain_percent, color) in enumerate(sample_data):
            stock_item = self.most_gains_items[index]
            stock_item.first_label.setText(symbol)
            stock_item.second_label.setText(f"${price}")
            stock_item.third_label.setText(f"${gain_value} ({gain_percent}%)")
            stock_item.third_label.setStyleSheet(f"color: {color};")
            stock_item.first_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            stock_item.second_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            stock_item.third_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def update_most_volume(self, sample_data):
        for index, (symbol, price, volume) in enumerate(sample_data):
            stock_item = self.most_volume_items[index]
            stock_item.first_label.setText(symbol)
            stock_item.second_label.setText(f"${price}")
            stock_item.third_label.setText(str(volume))

    def get_selected_stock(self):
        return self.stock_list.currentItem().text() if self.stock_list.currentItem() else None

    def set_dashboard_controller(self, controller):
        self.controller = controller

    def connect_buttons(self):
        self.logout_button.clicked.connect(self.controller.logout)
        self.search_bar.textChanged.connect(self.controller.update_suggestions)
        self.search_bar.returnPressed.connect(self.controller.search_stock)
        self.suggestion_list.itemClicked.connect(self.controller.select_suggestion)
        self.deposit_button.clicked.connect(self.controller.open_deposit_window)
        self.sell_button.clicked.connect(self.controller.handle_sell_button)
        self.stock_list.itemClicked.connect(self.controller.handle_portfolio_stock_clicked)

    def set_suggestions(self, suggestions):
        self.suggestion_list.clear()
        for suggestion in suggestions:
            if suggestion != 'Not found!':
                suggestion_text = suggestion[1] + f"\t({suggestion[0]})"
                QListWidgetItem(suggestion_text, self.suggestion_list)
            else:
                not_found_item = QListWidgetItem(suggestion, self.suggestion_list)
                not_found_item.setFlags(not_found_item.flags() & ~Qt.ItemIsSelectable)
                not_found_item.setForeground(Qt.gray)

        if suggestions:
            font_metrics = QFontMetrics(self.suggestion_list.font())
            text_height = font_metrics.height()

            self.suggestion_list.setGeometry(
                self.search_bar.geometry().adjusted(0, self.search_bar.height(),
                                                    0, (text_height + 5) * len(suggestions)))
            self.suggestion_list.setVisible(True)
        else:
            self.suggestion_list.setVisible(False)

    def get_search_text(self):
        return self.search_bar.text()

    def set_search_text(self, item):
        if item.flags() & Qt.ItemIsSelectable:
            self.search_bar.setText(item.text())
            self.suggestion_list.setVisible(False)

    def display_portfolio_stock_list(self, portfolio):
        self.stock_list.clear()
        if not portfolio:
            font = QFont()
            font.setPointSize(15)
            no_stocks_label = QLabel("You don't have anything in your portfolio.", self)
            no_stocks_label.setFont(font)
            no_stocks_label.setAlignment(Qt.AlignCenter)
            no_stocks_label.setStyleSheet("color: gray;")

            no_stocks_item = QListWidgetItem(self.stock_list)
            no_stocks_item.setSizeHint(no_stocks_label.sizeHint())
            no_stocks_item.setFlags(Qt.NoItemFlags)

            self.stock_list.addItem(no_stocks_item)
            self.stock_list.setItemWidget(no_stocks_item, no_stocks_label)
            self.stock_list.scrollToItem(no_stocks_item, QListWidget.PositionAtCenter)
        else:
            font = QFont()
            font.setPointSize(15)
            for stock in portfolio:
                item = QListWidgetItem(stock, self.stock_list)
                item.setFont(font)
                self.stock_list.addItem(item)

    def show_stock_not_found_message(self, stock):
        QMessageBox().warning(self, "Invalid stock name or symbol",
                              f"Couldn't find stock with given name or symbol: {stock}")

    def clear_view(self):
        self.search_bar.clear()
        self.stock_list.clear()
        self.suggestion_list.clear()


class StockItem(QWidget):
    def __init__(self, first_arg, second_arg, third_arg):
        super().__init__()

        self.first_label = QLabel(first_arg)
        self.first_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.second_label = QLabel(second_arg)
        self.second_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.third_label = QLabel(third_arg)
        self.third_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QHBoxLayout()
        layout.addWidget(self.first_label)
        layout.addWidget(self.second_label)
        layout.addWidget(self.third_label)

        self.setLayout(layout)
