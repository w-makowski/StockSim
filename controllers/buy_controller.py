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
        self.user_id = None
        
    def set_stock_symbol(self, stock_symbol):
        self.stock_symbol = stock_symbol

    def set_user_id(self, user_id):
        self.user_id = user_id
        
    def update_window(self):
        _, current_price, volume = self.market_service.get_stock_prices_and_volume(self.stock_symbol)
        self.current_price = current_price
        stock_name = self.market_service.get_stock_name(self.stock_symbol)
        self.buy_window.set_stock_current_price(self.current_price)
        self.buy_window.refresh_stock_amount_selector()
        self.buy_window.set_buy_stock_name(self.stock_symbol, stock_name)
        self.buy_window.set_stock_current_volume(volume)
        self.buy_window.set_total_price(0.00)

    def accept_purchase(self, amount, price):
        total_price_amount = amount * price
        if not isinstance(total_price_amount, Decimal):
            decimal_amount = Decimal(total_price_amount)
        else:
            decimal_amount = total_price_amount
        account_balance = self.user_service.get_user_balance(self.user_id)
        if account_balance < decimal_amount:
            self.buy_window.show_purchase_failure_message()
            self.buy_window.refresh_stock_amount_selector()
            return
        else:
            stock_id = self.market_service.get_stock_id(self.stock_symbol)
            self.user_service.update_user_portfolio(self.user_id, stock_id, amount, price, 'buy', datetime.utcnow())
            self.user_service.update_user_balance(self.user_id, account_balance - decimal_amount)
            self.buy_window.show_purchase_successful_message()
            self.buy_window.refresh_stock_amount_selector()

    def calculate_total_price(self, selected_amount):
        self.buy_window.set_total_price(self.current_price * selected_amount)
