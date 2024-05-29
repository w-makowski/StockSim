import re
from PySide6.QtWidgets import QMessageBox


class SignupController:
    def __init__(self, view, main_controller):
        self.view = view
        self.main_controller = main_controller
        self.user_service = main_controller.user_service

    def handle_signup(self):
        username = self.view.username_input.text()
        password = self.view.password_input.text()

        if not self.validate_username(username):
            self.view.feedback_label.setText("Incorrect Username")
            return

        if not self.validate_password(password):
            self.view.feedback_label.setText("Incorrect Password")
            self.view.password_input.clear()
            return

        if self.user_service.create_user(username, password):
            self.view.feedback_label.setText("Sign-up successful!")
            self.main_controller.show_login_view()
        else:
            self.view.feedback_label.setText("Sign-up failed! Username might already exist.")
            self.view.password_input.clear()

    def handle_back_button(self):
        self.view.username_input.clear()
        self.view.password_input.clear()
        self.view.feedback_label.setText("")
        self.main_controller.show_main_view()

    def validate_username(self, username):
        if not username:
            QMessageBox.warning(self.view, "Invalid Username", "Username field cannot be empty.")
            return False
        if not re.match(r'^[a-zA-Z0-9]{5,}$', username):
            QMessageBox.warning(self.view, "Invalid Username",
                                "Username must be at least 5 characters long and contain only alphanumeric characters without spaces.")
            return False

        return True

    def validate_password(self, password):
        if not password:
            QMessageBox.warning(self.view, "Invalid Password", "Password field cannot be empty.")
            return False

        if len(password) < 8:
            QMessageBox.warning(self.view, "Invalid Password",
                                "Password must be at least 8 characters long.")
            return False

        if not re.match(r'^[a-zA-Z0-9@#$%&?!_-]+$', password):
            QMessageBox.warning(self.view, "Invalid Password",
                                "Password can only contain alphanumeric characters and @#$%&?!_-")
            return False

        return True
