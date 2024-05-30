from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout, QHBoxLayout,
                               QLineEdit,
                               QLabel,
                               QPushButton,
                               QSizePolicy, QFrame)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class LoginView(QWidget):
    def __init__(self, main_controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login Form")

        self.main_controller = main_controller
        self.controller = None

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setStyleSheet("""
                    QFrame {
                        background-color: #212121;
                        border-radius: 15px;
                    }
                """)
        self.frame.setFixedSize(self.main_controller.main_window.width() / 2.2,
                                self.main_controller.main_window.height() / 1.5)

        self.login_label_font = QFont()
        # self.app_name_font.setFamily("Verdana Pro Cond Semibold")
        self.login_label_font.setPointSize(100)
        self.login_label_font.setBold(True)

        self.login_label = QLabel(self)
        self.login_label.setFont(self.login_label_font)
        self.login_label.setText("Login")
        self.login_label.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumWidth(300)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setMinimumWidth(300)

        self.feedback_label = QLabel("", self)
        self.feedback_label.setStyleSheet("color: red;")
        self.feedback_label.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton("Login", self)
        self.login_button.setMinimumWidth(120)

        self.back_button = QPushButton("Back", self)
        self.back_button.setMinimumWidth(120)

        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.login_label, alignment=Qt.AlignCenter)
        frame_layout.addSpacing(40)
        frame_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        frame_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        frame_layout.addWidget(self.feedback_label, alignment=Qt.AlignCenter)

        frame_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        frame_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        frame_layout.setAlignment(Qt.AlignCenter)

        self.frame.setLayout(frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def __del__(self):
        print("LoginView is being deleted")

    def set_login_controller(self, controller):
        self.controller = controller

    def connect_buttons(self):
        self.login_button.clicked.connect(self.controller.handle_login)
        self.back_button.clicked.connect(self.controller.handle_back_button)
