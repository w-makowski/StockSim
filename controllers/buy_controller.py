from decimal import Decimal
from datetime import datetime


class BuyController:
    def __init__(self, controller, buy_window=None, market_service=None, user_service=None):
        self.controller = controller
        self.buy_window = buy_window
        self.market_service = market_service
        self.user_service = user_service
        self.stock_symbol = None
        self.current_price = 0.00
        
    def set_stock_symbol(self, stock_symbol):
        self.stock_symbol = stock_symbol
        
    def update_window(self):
        _, current_price, volume = self.market_service.get_stock_prices_and_volume(self.stock_symbol)
        self.current_price = current_price
        stock_name = self.market_service.get_stock_name(self.stock_symbol)
        self.buy_window.set_stock_current_price(self.current_price)
        self.buy_window.set_buy_stock_name(self.stock_symbol, stock_name)
        self.buy_window.set_stock_current_volume(volume)
        self.buy_window.set_total_price(0.00)

    def accept_purchase(self, amount, price, user_id):
        total_price_amount = amount * price
        if isinstance(total_price_amount, float):
            decimal_amount = Decimal(total_price_amount)
        else:
            decimal_amount = Decimal(0)
        account_balance = self.user_service.get_user_balance(user_id)
        if account_balance < decimal_amount:
            self.buy_window.show_purchase_failure_message()
            return
        else:
            # whole procedure of buying
            stock_id = self.market_service.get_stock_id(self.stock_symbol)
            self.user_service.update_user_portfolio(user_id, stock_id, amount, price, 'buy', datetime.utcnow())
            self.user_service.update_user_balance(account_balance - decimal_amount)
            self.buy_window.show_purchase_successful_message()

    def validate_stock_amount(self, stock_amount):
        # or maybe at the beginning the max amount of stocks will be retrieving and setting as a limit to choose
        pass

    def calculate_total_price(self, selected_amount):
        self.buy_window.set_total_price(self.current_price * selected_amount)
