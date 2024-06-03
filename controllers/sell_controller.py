from collections import defaultdict
from decimal import Decimal


class SellController:
    def __init__(self, controller, sell_window=None, market_service=None, user_service=None):
        self.controller = controller
        self.sell_window = sell_window
        self.market_service = market_service
        self.user_service = user_service
        self.user_id = None

    def update_window(self, user_id):
        self.user_id = user_id
        self.sell_window.refresh_selector()
        self.sell_window.refresh_labels()
        portfolio = self.user_service.get_user_portfolio(user_id)
        stock_data = defaultdict(lambda: {'name': '', 'amount': 0})

        for transaction in portfolio:
            stock = self.market_service.get_stock(transaction.stock_id)
            stock_symbol = stock.symbol
            stock_name = stock.name
            stock_amount = transaction.amount

            stock_data[stock_symbol]['name'] = stock_name
            stock_data[stock_symbol]['amount'] += stock_amount
        print(stock_data)
        self.sell_window.refresh_sell_list(stock_data)

    def calculate_total_price(self, stock_symbol, stock_amount):
        current_price = self.get_sell_stock_current_price(stock_symbol)
        return current_price * stock_amount

    def get_sell_stock_current_price(self, stock_symbol):
        _, current_price, _ = self.market_service.get_stock_prices_and_volume(stock_symbol)
        return current_price

    def handle_sell(self, stock_symbol, stock_amount):
        stock_id = self.market_service.get_stock_id(stock_symbol)
        self.user_service.sell_stocks(self.user_id, stock_id, stock_amount)
        stock_price = self.get_sell_stock_current_price(stock_symbol)
        earning = stock_price * stock_amount
        if not isinstance(earning, Decimal):
            decimal_earning = Decimal(earning)
        else:
            decimal_earning = earning

        account_balance = self.user_service.get_user_balance(self.user_id)
        self.user_service.update_user_balance(self.user_id, account_balance + decimal_earning)

        self.controller.refresh_balance()
        self.controller.refresh_stock_list()
        self.update_window(self.user_id)
