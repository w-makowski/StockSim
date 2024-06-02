from gui.main_view import MainView
from gui.login_view import LoginView
from gui.signup_view import SignupView
from gui.dashboard_view import DashboardView
from gui.stock_view import StockView
from controllers.login_controller import LoginController
from controllers.signup_controller import SignupController
from controllers.dashboard_controller import DashboardController
from controllers.stock_controller import StockController
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
        self.stock_view = StockView(self)

        self.stack.addWidget(self.main_view)
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.signup_view)
        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.stock_view)

        # Initialize controllers
        self.login_controller = LoginController(self.login_view, self)
        self.signup_controller = SignupController(self.signup_view, self)
        self.dashboard_controller = DashboardController(self.dashboard_view, self)
        self.stock_controller = StockController(self.stock_view, self.market_service, self)

        self.main_view.connect_buttons()

        self.login_view.set_login_controller(self.login_controller)
        self.login_view.connect_buttons()

        self.signup_view.set_signup_controller(self.signup_controller)
        self.signup_view.connect_buttons()

        self.dashboard_view.set_dashboard_controller(self.dashboard_controller)
        self.dashboard_view.connect_buttons()

        self.stock_view.set_controller(self.stock_controller)
        self.stock_view.connect_buttons()

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

    def show_stock_view(self, stock_symbol):
        self.stack.setCurrentWidget(self.stock_view)
        self.stock_controller.update_stock(stock_symbol)

    def handle_logout(self):
        self.current_user = None
        self.show_main_view()

    def get_stock_symbols_and_names(self):
        stocks = []
        with open("resources/stocks_symbols.txt", 'r') as file:
            for line in file:
                line = line.replace("\n", "")
                elements = line.split("\t")
                stocks.append((elements[0], elements[1]))
        return stocks

    def add_stocks_to_db(self):
        self.market_service.add_new_stocks_to_db(self.get_stock_symbols_and_names())
