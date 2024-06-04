import yfinance as yf
from sqlalchemy import BigInteger
from models.stock import Stock
# from db.database import Database
from db.database import SessionLocal
from datetime import datetime
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP


class MarketService:
    def __init__(self):
        pass

    def fetch_stock_data(self, stock_symbol, period):
        intervals_for_period = {'1d': '1m', '5d': '5m', '3mo': '1d', '6mo': '1d',
                                'ytd': '1d', '1y': '1d', '5y': '1d', "max": '1d'}
        try:
            stock = yf.Ticker(stock_symbol)
            return stock.history(period=period, interval=intervals_for_period[period])
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None

    def fetch_stocks_data_for_db(self, stocks, period='5d', interval='1d'):
        tickers = ' '.join(stocks)
        data = yf.Tickers(tickers).history(period=period, interval=interval)
        return data

    def update_stocks_in_database(self):
        symbols = self.get_all_symbols()
        data1 = self.fetch_stocks_data_for_db(symbols[0:1000])
        data2 = self.fetch_stocks_data_for_db(symbols[1000:2000])
        data3 = self.fetch_stocks_data_for_db(symbols[2000:])
        data = pd.concat([data1, data2, data3], axis=1)
        session = SessionLocal()
        try:
            for symbol in symbols:
                data = data.fillna(0)
                if symbol not in data.columns.levels[1]:
                    print(f"No data found for {symbol}")
                    continue

                hist = data[('Close', symbol)]
                if len(hist) < 5:
                    print(f"Not enough data for {symbol}")
                    continue

                prev_day_close_price = hist.iloc[-2]
                current_price = hist.iloc[-1]
                current_volume = data[('Volume', symbol)].iloc[-1]
                current_datetime = datetime.utcnow()

                prev_day_close_price = prev_day_close_price if prev_day_close_price is not None else 0
                current_price = current_price if current_price is not None else 0
                current_volume = current_volume if current_volume is not None else 0

                stock = session.query(Stock).filter(Stock.symbol == symbol).first()
                if stock:
                    stock.prev_day_close_price = Decimal(prev_day_close_price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    stock.current_price = Decimal(current_price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    stock.current_volume = int(current_volume)
                    stock.current_datetime = current_datetime
                else:
                    print('Something wrong')
            session.commit()
        except Exception as e:
            session.rollback()
            print(f'An error occurred during updating stocks: {e}')
        finally:
            session.close()

    def get_all_symbols(self):
        session = SessionLocal()
        try:
            symbols = session.query(Stock.symbol).all()
            symbols = [item[0] for item in symbols]
            return symbols
        except Exception as e:
            print(f"An error occurred during getting stocks symbols form database: {e}")
            return []
        finally:
            session.close()

    def daily_stock_db_update(self):
        session = SessionLocal()
        try:
            last_update_date = session.query(Stock.current_datetime).filter(Stock.id == 1).first()[0]
            if datetime.utcnow().date() == last_update_date.date():
                print("Database updated")
                return False
            else:
                self.update_stocks_in_database()
        except Exception as e:
            print(f"Error retrieving last update date: {e}")
            return False
        finally:
            session.close()

    def add_new_stocks_to_db(self, new_stocks):
        session = SessionLocal()
        try:
            existing_symbols = {stock.symbol for stock in session.query(Stock.symbol).all()}
            stocks_to_add = [stock for stock in new_stocks if stock[0] not in existing_symbols]
            for symbol, name in stocks_to_add:
                new_stock = Stock(name=name, symbol=symbol, prev_day_close_price=0.00, current_price=0.00,
                                  current_volume=0, current_datetime=datetime.utcnow())
                session.add(new_stock)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error adding stock to database: {e}")
            return False
        finally:
            session.close()

    def get_stock_name(self, stock_symbol):
        session = SessionLocal()
        try:
            stock_name = session.query(Stock.name).filter(Stock.symbol == stock_symbol).first()[0]
            if stock_name:
                return stock_name
            return None
        except Exception as e:
            print(f"Error while retrieving stock name: {e}")
            return None
        finally:
            session.close()

    def get_stock_prices_and_volume(self, stock_symbol):
        session = SessionLocal()
        try:
            stock_name = (session.query(Stock.prev_day_close_price, Stock.current_price, Stock.current_volume).
                          filter(Stock.symbol == stock_symbol).first())
            if stock_name:
                return stock_name
            return None
        except Exception as e:
            print(f"Error while retrieving stock prices and volume: {e}")
            return None
        finally:
            session.close()

    def get_stock_id(self, stock_symbol):
        session = SessionLocal()
        try:
            stock_id = session.query(Stock.id).filter(Stock.symbol == stock_symbol).first()[0]
            if stock_id:
                return stock_id
            return None
        except Exception as e:
            print(f"Error while retrieving stock id: {e}")
            return None
        finally:
            session.close()

    def get_stock(self, stock_id):
        session = SessionLocal()
        try:
            stock = session.query(Stock).filter(Stock.id == stock_id).first()
            print(stock)
            if stock:
                return stock
            return None
        except Exception as e:
            print(f"Error while retrieving stock: {e}")
            return None
        finally:
            session.close()

    def get_biggest_gainers(self, number_of_gainers):
        def percentage_diff(value1, value2):
            if value2 == 0:
                return 0
            else:
                return ((value1 - value2) / value2) * 100
        session = SessionLocal()
        try:
            stocks = session.query(Stock).all()
            gainers = sorted(stocks, key=lambda x: percentage_diff(x.current_price, x.prev_day_close_price), reverse=True)
            biggest_gainers = gainers if number_of_gainers > len(gainers) else gainers[:number_of_gainers]
            return biggest_gainers
        except Exception as e:
            print(f"Error while retrieving stocks: {e}")
            return []
        finally:
            session.close()

    def get_highest_volumes(self, number_of_stocks):
        session = SessionLocal()
        try:
            stocks = session.query(Stock).all()
            stocks_sorted = sorted(stocks, key=lambda x: x.current_volume, reverse=True)
            highest_volumes = stocks_sorted if number_of_stocks > len(stocks_sorted) \
                else stocks_sorted[:number_of_stocks]
            return highest_volumes
        except Exception as e:
            print(f"Error while retrieving stocks: {e}")
            return []
        finally:
            session.close()
