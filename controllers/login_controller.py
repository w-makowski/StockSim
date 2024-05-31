class LoginController:
    def __init__(self, view, main_controller):
        self.view = view
        self.main_controller = main_controller
        self.user_service = main_controller.user_service

    def handle_login(self):
        username = self.view.username_input.text()
        password = self.view.password_input.text()
        user = self.user_service.authenticate(username, password)
        if user:
            # Transition to dashboard
            self.main_controller.handle_login_success(user)
            self.__clear_view()
        else:
            # Error - login failed
            self.__clear_view()
            self.view.feedback_label.setText("Login failed! Invalid username or password.")

    def handle_back_button(self):
        self.__clear_view()
        self.main_controller.show_main_view()

    def __clear_view(self):
        self.view.username_input.clear()
        self.view.password_input.clear()
        self.view.feedback_label.setText("")
