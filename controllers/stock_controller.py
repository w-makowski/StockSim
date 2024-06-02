from controllers.buy_controller import BuyController
from gui.buy_window import BuyWindow


class StockController:
    def __init__(self, view, market_service, main_controller):
        self.view = view
        self.market_service = market_service
        self.main_controller = main_controller
        self.stock_symbol = None

        self.buy_window = BuyWindow(parent=self.main_controller.main_window)
        self.buy_controller = BuyController(self, self.buy_window, self.market_service,
                                            self.main_controller.user_service)
        self.buy_window.set_controller(self.buy_controller)
        self.buy_window.connect_buttons()

    def refresh_chart(self, period):
        # chart_data = self.market_service.get_latest_data(self.stock_symbol)
        # self.view.update_chart(chart_data)
        if self.stock_symbol:
            data = self.market_service.fetch_stock_data(self.stock_symbol, period)
            if data is not None and not data.empty:
                self.view.update_chart(data, self.stock_symbol, period)

    def update_stock(self, stock_symbol):
        # main function to update everything
        self.stock_symbol = stock_symbol
        # self.view.update_view_for_stock(stock_symbol)
        self.update_stock_name()
        self.update_stock_prices_and_volume()
        self.refresh_chart('1d')

    def update_stock_name(self):
        stock_name = self.market_service.get_stock_name(self.stock_symbol)
        self.view.set_stock_name(self.stock_symbol, stock_name)

    def update_stock_prices_and_volume(self):
        current_stock_value, prev_stock_value, volume = (self.market_service.
                                                         get_stock_prices_and_volume(self.stock_symbol))
        value_diff = current_stock_value - prev_stock_value
        if prev_stock_value != 0:
            value_diff_proc = (value_diff / prev_stock_value) * 100
        else:
            value_diff_proc = 0
        self.view.set_stock_value(current_stock_value, value_diff, value_diff_proc)
        self.view.set_stock_volume(volume)

    def handle_buy_stock(self):
        self.buy_controller.set_stock_symbol(self.stock_symbol)
        self.buy_controller.update_window()
        self.buy_window.exec()

