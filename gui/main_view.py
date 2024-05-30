from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLineEdit,
                               QLabel,
                               QPushButton,
                               QSizePolicy)
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtCore import Qt


VERSION = 'v1.0'
AUTHOR = 'Wojciech Makowski'


class MainView(QWidget):
    def __init__(self, main_controller):
        super().__init__()
        self.main_controller = main_controller

        self.login_button = QPushButton("Login", self)
        self.signup_button = QPushButton("SignUp", self)
        self.login_button.setMinimumWidth(55)
        self.signup_button.setMinimumWidth(55)

        self.login_services_buttons_layout = QHBoxLayout()
        self.login_services_buttons_layout.addWidget(self.login_button)
        self.login_services_buttons_layout.addWidget(self.signup_button)
        self.login_services_buttons_layout.setAlignment(Qt.AlignRight)

        self.logo_label = QLabel(self)
        pixmap = QPixmap("resources/StockSim_logo.png")
        if pixmap.isNull():
            print("Failed to load image.")
        else:
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setAlignment(Qt.AlignHCenter)

        self.app_name_font = QFont()
        #self.app_name_font.setFamily("Verdana Pro Cond Semibold")
        self.app_name_font.setPointSize(120)
        self.app_name_font.setBold(True)

        self.app_name_label = QLabel(self)
        self.app_name_label.setFont(self.app_name_font)
        self.app_name_label.setAlignment(Qt.AlignHCenter)
        self.app_name_label.setText("StockSim")

        self.logo_layout = QVBoxLayout()
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        self.logo_layout.addWidget(self.app_name_label, alignment=Qt.AlignCenter)
        #self.logo_layout.setAlignment(Qt.AlignCenter)

        self.version_label = QLabel(f'Version: {VERSION}', self)
        self.version_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.author_label = QLabel(f'Author: {AUTHOR}', self)
        self.author_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.author_version_layout = QHBoxLayout()
        self.author_version_layout.addWidget(self.version_label, alignment=Qt.AlignBottom  | Qt.AlignLeft)
        self.author_version_layout.addWidget(self.author_label, alignment=Qt.AlignBottom | Qt.AlignRight)

        layout = QVBoxLayout()
        layout.addLayout(self.login_services_buttons_layout)
        layout.addSpacing(self.main_controller.main_window.height()/6)
        layout.addLayout(self.logo_layout)
        layout.addLayout(self.author_version_layout)

        self.setLayout(layout)

    def connect_buttons(self):
        self.login_button.clicked.connect(self.main_controller.show_login_view)
        self.signup_button.clicked.connect(self.main_controller.show_signup_view)
