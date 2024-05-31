from gui.main_view import MainView
from gui.login_view import LoginView
from gui.signup_view import SignupView
from gui.dashboard_view import DashboardView
from gui.stock_chart_view import StockChartView
from controllers.login_controller import LoginController
from controllers.signup_controller import SignupController
from controllers.dashboard_controller import DashboardController
from controllers.stock_chart_controller import StockChartController
from services.user_service import UserService
from services.market_service import MarketService
from PySide6.QtWidgets import QStackedWidget


class MainController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.user_service = UserService()
        self.market_service = MarketService()

        self.stack = QStackedWidget(self.main_window)
        self.main_window.setCentralWidget(self.stack)

        # Initialize views
        self.main_view = MainView(self)
        self.login_view = LoginView(self, parent=self.stack)
        self.signup_view = SignupView(self)
        self.dashboard_view = DashboardView(self)
        self.stock_chart_view = StockChartView(None)  # Set the controller later

        self.stack.addWidget(self.main_view)
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.signup_view)
        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.stock_chart_view)

        # Initialize controllers
        self.login_controller = LoginController(self.login_view, self)
        self.signup_controller = SignupController(self.signup_view, self)
        self.dashboard_controller = DashboardController(self.dashboard_view, self)
        self.stock_chart_controller = StockChartController(self.stock_chart_view, self.market_service)
        self.stock_chart_view.controller = self.stock_chart_controller  # Link controller to view

        self.main_view.connect_buttons()

        self.login_view.set_login_controller(self.login_controller)
        self.login_view.connect_buttons()

        self.signup_view.set_signup_controller(self.signup_controller)
        self.signup_view.connect_buttons()

        self.dashboard_view.set_dashboard_controller(self.dashboard_controller)
        self.dashboard_view.connect_buttons(self)

        self.current_user = None

    def show_main_view(self):
        self.stack.setCurrentWidget(self.main_view)

    def show_login_view(self):
        self.stack.setCurrentWidget(self.login_view)

    def show_signup_view(self):
        self.stack.setCurrentWidget(self.signup_view)

    def show_dashboard_view(self):
        self.stack.setCurrentWidget(self.dashboard_view)
        self.dashboard_controller.update_dashboard(self.current_user)

    def handle_login_success(self, user):
        self.current_user = user
        self.show_dashboard_view()

    def show_stock_chart_view(self, stock_name):
        self.stack.setCurrentWidget(self.stock_chart_view)
        self.stock_chart_controller.refresh_chart(stock_name)

    def handle_logout(self):
        self.current_user = None
        self.show_main_view()
