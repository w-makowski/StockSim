from datetime import datetime
from controllers.deposit_controller import DepositController
from controllers.sell_controller import SellController
from gui.deposit_window import DepositWindow
from gui.sell_window import SellWindow
from decimal import Decimal


class DashboardController:
    def __init__(self, view, main_controller):
        self.view = view
        self.main_controller = main_controller
        self.user = None
        self.user_service = main_controller.user_service
        self.market_service = main_controller.market_service
        self.searching_values = self.get_stock_symbols_and_names()

        self.deposit_window = DepositWindow(parent=self.main_controller.main_window)
        self.deposit_controller = DepositController(self, self.deposit_window)
        self.deposit_window.set_deposit_controller(self.deposit_controller)
        self.deposit_window.connect_buttons()

        self.sell_window = SellWindow(parent=self.main_controller.main_window)
        self.sell_controller = SellController(self, self.sell_window, self.market_service, self.user_service)
        self.sell_window.set_sell_controller(self.sell_controller)
        self.sell_window.connect_buttons()

    def update_dashboard(self, user):
        self.user = user
        self.view.user_greeting_label.setText(f"Welcome {self.user.username}!")

        self.refresh_balance()
        self.refresh_stock_list()

        self.refresh_most_gains()
        self.refresh_most_volume()

    def update_suggestions(self):
        text = self.view.get_search_text()
        if text:
            matches = [item for item in self.searching_values.items()
                       if any(text.lower() in pair_item.lower() for pair_item in item)][:5]
            if not matches:
                matches = ['Not found!']
            self.view.set_suggestions(matches)
        else:
            self.view.set_suggestions([])

    def select_suggestion(self, item):
        self.view.set_search_text(item)
        self.search_stock()

    def search_stock(self):
        text = self.view.get_search_text()
        text = text.split("\t")[0]
        if text.upper() in self.searching_values.values():
            # text is a symbol
            self.view.search_bar.clear()
            self.main_controller.show_stock_view(text.upper())
        else:
            searching_values_lower = {key.lower(): value for key, value in self.searching_values.items()}
            key_lower = text.lower()
            if key_lower in searching_values_lower:
                stock_symbol = searching_values_lower[key_lower]
                self.view.search_bar.clear()
                self.main_controller.show_stock_view(stock_symbol)
                pass
            else:
                self.view.show_stock_not_found_message(text)
                self.view.search_bar.clear()

    def handle_portfolio_stock_clicked(self):
        selected_stock = self.view.stock_list.selectedItems()[0]
        stock_symbol = selected_stock.text().split("\t")[1]
        self.main_controller.show_stock_view(stock_symbol)

    def refresh_stock_list(self):
        portfolio = self.user_service.get_user_portfolio(self.user.id)
        portfolio_list = []
        self.view.stock_list.clear()
        if portfolio:
            for transaction in portfolio:
                stock_id = transaction.stock_id
                stock = self.market_service.get_stock(stock_id)
                stock_symbol = stock.symbol
                stock_name = stock.name
                transaction_date = transaction.transaction_datetime.strftime("%d-%m-%Y %H:%M")
                transaction_amount = transaction.amount
                transaction_price = transaction.price
                portfolio_list.append(f'{transaction_date}\t{stock_symbol}\t${transaction_price}\t{transaction_amount}\t({stock_name})')
            self.view.display_portfolio_stock_list(portfolio_list)
        else:
            self.view.display_portfolio_stock_list(portfolio)

    def refresh_balance(self):
        balance = self.user_service.get_user_balance(self.user.id)
        self.view.set_user_balance(balance)

    def refresh_most_gains(self):
        biggest_gainers = self.market_service.get_biggest_gainers(20)
        sample_data = []
        for stock in biggest_gainers:
            price_diff = stock.current_price - stock.prev_day_close_price
            price_diff_percent = 0.0 if stock.prev_day_close_price == 0 else (
                    (price_diff / stock.prev_day_close_price) * 100)
            price_diff_percent = round(price_diff_percent, 2)
            if price_diff >= 0:
                sign = '+'
                color = 'white' if price_diff == 0 else 'green'
            else:
                sign = '-'
                color = 'red'
            sample_data.append((stock.symbol, stock.current_price, f'{sign}{price_diff}', f'{sign}{price_diff_percent}', color))
        print(sample_data)
        self.view.update_most_gains(sample_data)

    def refresh_most_volume(self):
        highest_volumes = self.market_service.get_highest_volumes(20)
        sample_data = [(stock.symbol, stock.current_price, stock.current_volume) for stock in highest_volumes]
        print(sample_data)
        self.view.update_most_volume(sample_data)

    def make_a_deposit(self, deposit):
        current_balance = self.user_service.get_user_balance(self.user.id)
        if isinstance(deposit, float):
            decimal_deposit = Decimal(deposit)
        else:
            decimal_deposit = Decimal(0)
        self.user_service.update_user_balance(self.user.id, current_balance + decimal_deposit)
        self.refresh_balance()

    def open_deposit_window(self):
        self.deposit_window.exec()

    def logout(self):
        self.view.clear_view()
        self.main_controller.handle_logout()

    def get_stock_symbols_and_names(self):
        dictionary = {}
        with open("resources/stocks_symbols.txt", 'r') as file:
            for line in file:
                line = line.replace("\n", "")
                elements = line.split("\t")
                dictionary[elements[1]] = elements[0]
        print(dictionary)
        return dictionary

    def handle_sell_button(self):
        self.sell_controller.update_window(self.user.id)
        self.sell_window.exec()
