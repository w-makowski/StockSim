import re


class DepositController:
    def __init__(self, controller, deposit_window=None):
        self.controller = controller
        self.deposit_window = deposit_window

    def validate_deposit_amount(self, text):
        pattern = r'^\d{1,10}(\,\d{1,2}|\.\d{1,2})?$'
        return bool(re.match(pattern, text))

    def accept_deposit(self):
        deposit_amount = self.deposit_window.deposit_input.text()
        if self.validate_deposit_amount(deposit_amount):
            try:
                deposit_amount = deposit_amount.replace(',', '.')
                deposit = float(deposit_amount)
                if deposit < 0:
                    self.deposit_window.show_popup_message("Deposit amount must be non-negative.")
                    return
                else:
                    self.deposit_window.close()
                    self.controller.make_a_deposit(deposit)
            except ValueError:
                self.deposit_window.show_popup_message("Invalid deposit amount. Please enter a valid number.")
                return
            finally:
                self.deposit_window.deposit_input.clear()
        else:
            self.deposit_window.show_popup_message("Invalid deposit amount.\nMaximum of 2 digits after comma or period.")
            self.deposit_window.deposit_input.clear()
            return
