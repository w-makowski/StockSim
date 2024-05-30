from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout, QGroupBox, QFrame,
                               QLineEdit,
                               QLabel,
                               QPushButton,
                               QSizePolicy)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class SignupView(QWidget):
    def __init__(self, main_controller):
        super().__init__()
        self.setWindowTitle("Sign Up Form")

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
        self.frame.setFixedSize(self.main_controller.main_window.width()/2.2,
                                self.main_controller.main_window.height()/1.5)

        self.signup_label_font = QFont()
        # self.app_name_font.setFamily("Verdana Pro Cond Semibold")
        self.signup_label_font.setPointSize(100)
        self.signup_label_font.setBold(True)

        self.signup_label = QLabel(self)
        self.signup_label.setFont(self.signup_label_font)
        self.signup_label.setText("Sign Up")
        self.signup_label.setAlignment(Qt.AlignCenter)

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

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.setMinimumWidth(120)

        self.back_button = QPushButton("Back", self)
        self.back_button.setMinimumWidth(120)

        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.signup_label, alignment=Qt.AlignCenter)
        frame_layout.addSpacing(40)
        frame_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        frame_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        frame_layout.addWidget(self.feedback_label, alignment=Qt.AlignCenter)
        frame_layout.addWidget(self.signup_button, alignment=Qt.AlignCenter)
        frame_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        frame_layout.setAlignment(Qt.AlignCenter)

        self.frame.setLayout(frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def set_signup_controller(self, controller):
        self.controller = controller

    def connect_buttons(self):
        self.signup_button.clicked.connect(self.controller.handle_signup)
        self.back_button.clicked.connect(self.controller.handle_back_button)
