from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class DepositWindow(QDialog):
    def __init__(self, parent=None, deposit_controller=None):
        super().__init__(parent)
        self.setWindowTitle("Make a Deposit")

        self.setFixedSize(400, 400)

        self.parent = parent
        self.deposit_controller = deposit_controller

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: #212121;
                border-radius: 15px;
            }
        """)
        self.frame.setFixedSize(250, 250)

        frame_layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(32)

        self.deposit_label = QLabel("Make a deposit")
        self.deposit_label.setFont(font)
        self.deposit_input = QLineEdit(self)
        self.deposit_input.setPlaceholderText("Enter deposit amount")

        self.cancel_button = QPushButton("Cancel", self)
        self.accept_button = QPushButton("Accept", self)
        self.accept_button.setEnabled(False)

        self.deposit_input.textChanged.connect(self.toggle_accept_button)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.accept_button)
        self.buttons_layout.setAlignment(Qt.AlignBottom)

        frame_layout.addWidget(self.deposit_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        frame_layout.addSpacing(110)
        frame_layout.addWidget(self.deposit_input, alignment=Qt.AlignVCenter)
        frame_layout.addSpacing(110)
        frame_layout.addLayout(self.buttons_layout)
        frame_layout.setAlignment(Qt.AlignCenter)

        self.frame.setLayout(frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def toggle_accept_button(self):
        self.accept_button.setEnabled(bool(self.deposit_input.text()))

    def set_deposit_controller(self, deposit_controller):
        self.deposit_controller = deposit_controller

    def connect_buttons(self):
        self.cancel_button.clicked.connect(self.close)
        self.accept_button.clicked.connect(self.deposit_controller.accept_deposit)

    def show_popup_message(self, text):
        QMessageBox().warning(self, "Invalid deposit amount", text)
